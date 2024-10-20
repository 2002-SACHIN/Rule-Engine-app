import re
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from .models import Rule, Node, Attribute

def create_rule(db: Session, rule_string: str, name: str, description: str = "") -> Rule:
    tokens = tokenize_rule(rule_string)
    ast = parse_tokens(tokens)
    rule = Rule(name=name, description=description)
    db.add(rule)
    db.flush()  # Get the rule ID
    root_node = create_node_from_ast(db, ast, rule.id)
    rule.root_node = root_node
    db.commit()
    return rule

def tokenize_rule(rule_string: str) -> List[str]:
    return re.findall(r'\(|\)|AND|OR|[<>=]+|\w+|\d+', rule_string)

def parse_tokens(tokens: List[str]) -> Dict:
    def parse_expression():
        if tokens[0] == '(':
            tokens.pop(0)  # Remove opening parenthesis
            left = parse_expression()
            op = tokens.pop(0)
            right = parse_expression()
            tokens.pop(0)  # Remove closing parenthesis
            return {'type': 'operator', 'operator': op, 'left': left, 'right': right}
        else:
            return {'type': 'operand', 'left': tokens.pop(0), 'operator': tokens.pop(0), 'right': tokens.pop(0)}

    return parse_expression()

def create_node_from_ast(db: Session, ast: Dict, rule_id: int) -> Node:
    node = Node(type=ast['type'], rule_id=rule_id)
    if ast['type'] == 'operator':
        node.operator = ast['operator']
        db.add(node)
        db.flush()  # Get the node ID
        node.left_child = create_node_from_ast(db, ast['left'], rule_id)
        node.right_child = create_node_from_ast(db, ast['right'], rule_id)
    else:  # operand
        node.value = f"{ast['left']} {ast['operator']} {ast['right']}"
    db.add(node)
    return node

def combine_rules(db: Session, rule_ids: List[int], new_rule_name: str) -> Rule:
    rules = db.query(Rule).filter(Rule.id.in_(rule_ids)).all()
    combined_ast = {'type': 'operator', 'operator': 'AND', 'left': None, 'right': None}
    
    for rule in rules:
        if combined_ast['left'] is None:
            combined_ast['left'] = rule.root_node
        elif combined_ast['right'] is None:
            combined_ast['right'] = rule.root_node
        else:
            combined_ast = {'type': 'operator', 'operator': 'AND', 'left': combined_ast, 'right': rule.root_node}

    new_rule = Rule(name=new_rule_name)
    db.add(new_rule)
    db.flush()  # Get the new rule ID
    root_node = create_node_from_ast(db, combined_ast, new_rule.id)
    new_rule.root_node = root_node
    db.commit()
    return new_rule

def evaluate_rule(db: Session, rule_id: int, data: Dict[str, Any]) -> bool:
    rule = db.query(Rule).filter(Rule.id == rule_id).first()
    if not rule:
        raise ValueError("Rule not found")

    def evaluate_node(node: Node) -> bool:
        if node.type == 'operator':
            left_result = evaluate_node(node.left_child)
            right_result = evaluate_node(node.right_child)
            if node.operator == 'AND':
                return left_result and right_result
            elif node.operator == 'OR':
                return left_result or right_result
        else:  # operand
            attr, op, value = node.value.split()
            if attr not in data:
                raise ValueError(f"Attribute '{attr}' not found in data")
            if op == '=':
                return data[attr] == value
            elif op == '>':
                return data[attr] > float(value)
            elif op == '<':
                return data[attr] < float(value)
            else:
                raise ValueError(f"Unsupported operator: {op}")

    return evaluate_node(rule.root_node)
