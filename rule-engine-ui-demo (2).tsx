import React, { useState } from 'react';
import { XAxis, YAxis, CartesianGrid, Tooltip, Legend, BarChart, Bar, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle, XCircle } from 'lucide-react';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

const DemoDashboard = () => {
  const [rules, setRules] = useState([
    { id: 1, name: "Age Rule", description: "Check if age is over 18", rule_string: "age > 18" },
    { id: 2, name: "Income Rule", description: "Check if income is over 50000", rule_string: "income > 50000" },
  ]);
  const [newRule, setNewRule] = useState({ name: '', description: '', rule_string: '' });
  const [evaluationData, setEvaluationData] = useState('');
  const [evaluationResult, setEvaluationResult] = useState(null);

  const handleCreateRule = (e) => {
    e.preventDefault();
    setRules([...rules, { ...newRule, id: rules.length + 1 }]);
    setNewRule({ name: '', description: '', rule_string: '' });
  };

  const handleDeleteRule = (id) => {
    setRules(rules.filter(rule => rule.id !== id));
  };

  const handleEvaluateRule = () => {
    setEvaluationResult(Math.random() < 0.5);
  };

  const chartData = rules.map(rule => ({
    name: rule.name,
    complexity: rule.rule_string.length,
  }));

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6">Rule Engine Dashboard</h1>
      
      <Button className="mb-4" onClick={() => alert('Rules refreshed!')}>Refresh Rules</Button>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Create New Rule</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleCreateRule} className="space-y-4">
              <Input
                type="text"
                placeholder="Rule Name"
                value={newRule.name}
                onChange={(e) => setNewRule({...newRule, name: e.target.value})}
              />
              <Input
                type="text"
                placeholder="Rule Description"
                value={newRule.description}
                onChange={(e) => setNewRule({...newRule, description: e.target.value})}
              />
              <Textarea
                placeholder="Rule String"
                value={newRule.rule_string}
                onChange={(e) => setNewRule({...newRule, rule_string: e.target.value})}
              />
              <Button type="submit">Create Rule</Button>
            </form>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Evaluate Rule</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Textarea
                placeholder="Enter JSON data for evaluation"
                value={evaluationData}
                onChange={(e) => setEvaluationData(e.target.value)}
              />
              <div className="flex flex-wrap gap-2">
                {rules.map(rule => (
                  <Button key={rule.id} onClick={handleEvaluateRule}>
                    Evaluate {rule.name}
                  </Button>
                ))}
              </div>
              {evaluationResult !== null && (
                <Alert variant={evaluationResult ? "default" : "destructive"}>
                  {evaluationResult ? <CheckCircle className="h-4 w-4" /> : <XCircle className="h-4 w-4" />}
                  <AlertTitle>Evaluation Result</AlertTitle>
                  <AlertDescription>
                    {evaluationResult ? "Rule conditions met" : "Rule conditions not met"}
                  </AlertDescription>
                </Alert>
              )}
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Existing Rules</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {rules.map(rule => (
              <div key={rule.id} className="flex items-center justify-between p-4 bg-gray-100 rounded">
                <div>
                  <h3 className="font-semibold">{rule.name}</h3>
                  <p className="text-sm text-gray-600">{rule.description}</p>
                  <p className="text-xs text-gray-500">{rule.rule_string}</p>
                </div>
                <Button variant="destructive" onClick={() => handleDeleteRule(rule.id)}>Delete</Button>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <Card className="mt-6">
        <CardHeader>
          <CardTitle>Rule Complexity Chart</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="complexity" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  );
};

export default DemoDashboard;
