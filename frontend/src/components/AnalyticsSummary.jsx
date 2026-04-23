import React from 'react';
import { DollarSign, BarChart3, Receipt } from 'lucide-react';

export default function AnalyticsSummary({ data }) {
  if (!data) return null;

  const cards = [
    {
      title: 'Total Spent',
      value: `$${data.total_spent.toLocaleString()}`,
      icon: <DollarSign className="w-6 h-6 text-green-600" />,
      bg: 'bg-green-50'
    },
    {
      title: 'Total Receipts',
      value: data.expense_count,
      icon: <Receipt className="w-6 h-6 text-blue-600" />,
      bg: 'bg-blue-50'
    },
    {
      title: 'Top Category',
      value: Object.keys(data.category_breakdown).length > 0 
        ? Object.entries(data.category_breakdown).sort((a,b) => b[1] - a[1])[0][0]
        : 'N/A',
      icon: <BarChart3 className="w-6 h-6 text-purple-600" />,
      bg: 'bg-purple-50'
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
      {cards.map((card, i) => (
        <div key={i} className="card flex items-center gap-4">
          <div className={`${card.bg} p-3 rounded-xl`}>
            {card.icon}
          </div>
          <div>
            <p className="text-sm text-gray-500 font-medium">{card.title}</p>
            <p className="text-2xl font-bold text-gray-900">{card.value}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
