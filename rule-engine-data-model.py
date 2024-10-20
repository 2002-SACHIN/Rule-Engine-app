from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Rule(Base):
    __tablename__ = 'rules'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    root_node_id = Column(Integer, ForeignKey('nodes.id'))
    root_node = relationship("Node", back_populates="rule")

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)  # 'operator' or 'operand'
    value = Column(String)  # For operands: attribute name or literal value
    operator = Column(String)  # For operators: 'AND', 'OR', '>', '<', '=', etc.
    rule_id = Column(Integer, ForeignKey('rules.id'))
    rule = relationship("Rule", back_populates="root_node")
    left_child_id = Column(Integer, ForeignKey('nodes.id'))
    right_child_id = Column(Integer, ForeignKey('nodes.id'))
    left_child = relationship("Node", foreign_keys=[left_child_id], remote_side=[id])
    right_child = relationship("Node", foreign_keys=[right_child_id], remote_side=[id])

class Attribute(Base):
    __tablename__ = 'attributes'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    data_type = Column(String, nullable=False)  # 'string', 'integer', 'float', etc.
    is_active = Column(Boolean, default=True)
