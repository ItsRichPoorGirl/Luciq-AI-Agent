'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { CalendarIcon, Download, Search } from 'lucide-react';

interface UsageLogsProps {
  accountId: string;
}

export default function UsageLogs({ accountId }: UsageLogsProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPeriod, setSelectedPeriod] = useState('7d');
  const [selectedModel, setSelectedModel] = useState('all');

  // Mock data - replace with actual API call
  const usageData = [
    {
      id: 1,
      date: new Date(),
      model: 'GPT-4o',
      tokens: 1250,
      cost: 0.025,
      type: 'completion'
    },
    {
      id: 2,
      date: new Date(Date.now() - 86400000),
      model: 'Claude 3.5 Sonnet',
      tokens: 890,
      cost: 0.018,
      type: 'completion'
    },
    {
      id: 3,
      date: new Date(Date.now() - 172800000),
      model: 'Gemini 2.5 Pro',
      tokens: 2100,
      cost: 0.042,
      type: 'completion'
    }
  ];

  const totalUsage = usageData.reduce((sum, item) => sum + item.cost, 0);
  const totalTokens = usageData.reduce((sum, item) => sum + item.tokens, 0);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Usage Logs</h1>
          <p className="text-muted-foreground">
            Monitor your AI model usage and costs
          </p>
        </div>
        <Button variant="outline" size="sm">
          <Download className="mr-2 h-4 w-4" />
          Export
        </Button>
      </div>

      {/* Summary Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Cost</CardTitle>
            <Badge variant="secondary">This Month</Badge>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalUsage.toFixed(3)}</div>
            <p className="text-xs text-muted-foreground">
              +2.1% from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Tokens</CardTitle>
            <Badge variant="secondary">This Month</Badge>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalTokens.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">
              +5.2% from last month
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Most Used Model</CardTitle>
            <Badge variant="secondary">This Month</Badge>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">GPT-4o</div>
            <p className="text-xs text-muted-foreground">
              45% of total usage
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Usage Table */}
      <Card>
        <CardHeader>
          <CardTitle>Usage History</CardTitle>
          <CardDescription>
            Detailed breakdown of your AI model usage
          </CardDescription>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Date</TableHead>
                <TableHead>Model</TableHead>
                <TableHead>Tokens</TableHead>
                <TableHead>Cost</TableHead>
                <TableHead>Type</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {usageData.map((item) => (
                <TableRow key={item.id}>
                  <TableCell>
                    <div className="flex items-center">
                      <CalendarIcon className="mr-2 h-4 w-4 text-muted-foreground" />
                      {item.date.toLocaleDateString()}
                    </div>
                  </TableCell>
                  <TableCell>
                    <Badge variant="outline">{item.model}</Badge>
                  </TableCell>
                  <TableCell>{item.tokens.toLocaleString()}</TableCell>
                  <TableCell>${item.cost.toFixed(3)}</TableCell>
                  <TableCell>
                    <Badge variant="secondary">{item.type}</Badge>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
