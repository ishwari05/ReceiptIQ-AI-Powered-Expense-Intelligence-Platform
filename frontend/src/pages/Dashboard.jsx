import React, { useEffect, useState } from 'react';
import api from '../services/api';
import AnalyticsSummary from '../components/AnalyticsSummary';
import ExpenseTable from '../components/ExpenseTable';
import { Loader2, Plus, Search, Filter } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Dashboard() {
  const [expenses, setExpenses] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  const fetchData = async () => {
    try {
      const [expRes, anaRes] = await Promise.all([
        api.get('/expenses/'),
        api.get('/expenses/analytics')
      ]);
      setExpenses(expRes.data);
      setAnalytics(anaRes.data);
    } catch (err) {
      console.error("Failed to fetch data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredExpenses = expenses.filter(exp => 
    exp.vendor?.toLowerCase().includes(search.toLowerCase()) ||
    exp.category?.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex items-center justify-center h-[80vh]">
        <Loader2 className="w-10 h-10 animate-spin text-primary-600" />
      </div>
    );
  }

  return (
    <div className="space-y-10">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">Monitor your spending and manage receipts</p>
        </div>
        <button 
          onClick={() => navigate('/upload')}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Add Receipt
        </button>
      </div>

      <AnalyticsSummary data={analytics} />

      <div className="space-y-6">
        <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900">Expenses</h2>
          
          <div className="flex gap-4 w-full md:w-auto">
            <div className="relative flex-1 md:w-80">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
              <input 
                type="text"
                placeholder="Search vendor or category..."
                className="input-field pl-9 py-2 text-sm"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <button className="px-4 py-2 border border-gray-200 rounded-lg flex items-center gap-2 text-sm font-medium hover:bg-gray-50">
              <Filter className="w-4 h-4" />
              Filters
            </button>
          </div>
        </div>

        <ExpenseTable expenses={filteredExpenses} onUpdate={fetchData} />
      </div>
    </div>
  );
}
