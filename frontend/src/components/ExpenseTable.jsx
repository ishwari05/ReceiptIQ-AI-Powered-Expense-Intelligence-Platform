import React, { useState } from 'react';
import { Edit2, Trash2, Calendar, Tag, MoreVertical, Check, X } from 'lucide-react';
import api from '../services/api';

export default function ExpenseTable({ expenses, onUpdate }) {
  const [editingId, setEditingId] = useState(null);
  const [editData, setEditData] = useState({});

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this expense?')) {
      try {
        await api.delete(`/expenses/${id}`);
        onUpdate();
      } catch (err) {
        alert('Failed to delete expense');
      }
    }
  };

  const startEditing = (expense) => {
    setEditingId(expense.id);
    setEditData({
      vendor: expense.vendor,
      amount: expense.amount,
      category: expense.category,
      date: expense.date ? new Date(expense.date).toISOString().split('T')[0] : ''
    });
  };

  const handleUpdate = async (id) => {
    try {
      await api.put(`/expenses/${id}`, editData);
      setEditingId(null);
      onUpdate();
    } catch (err) {
      alert('Failed to update expense');
    }
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <table className="w-full text-left">
        <thead>
          <tr className="bg-gray-50 border-b border-gray-200">
            <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Vendor</th>
            <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Amount</th>
            <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Date</th>
            <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase">Category</th>
            <th className="px-6 py-4 text-xs font-semibold text-gray-500 uppercase text-right">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {expenses.map((expense) => (
            <tr key={expense.id} className="hover:bg-gray-50 transition-colors">
              <td className="px-6 py-4">
                {editingId === expense.id ? (
                  <input 
                    className="input-field py-1"
                    value={editData.vendor}
                    onChange={(e) => setEditData({...editData, vendor: e.target.value})}
                  />
                ) : (
                  <span className="font-medium text-gray-900">{expense.vendor || 'Unknown'}</span>
                )}
              </td>
              <td className="px-6 py-4">
                {editingId === expense.id ? (
                  <input 
                    type="number"
                    className="input-field py-1"
                    value={editData.amount}
                    onChange={(e) => setEditData({...editData, amount: parseFloat(e.target.value)})}
                  />
                ) : (
                  <span className="text-gray-900">${expense.amount?.toFixed(2)}</span>
                )}
              </td>
              <td className="px-6 py-4">
                {editingId === expense.id ? (
                  <input 
                    type="date"
                    className="input-field py-1"
                    value={editData.date}
                    onChange={(e) => setEditData({...editData, date: e.target.value})}
                  />
                ) : (
                  <div className="flex items-center gap-2 text-gray-500">
                    <Calendar className="w-4 h-4" />
                    {expense.date ? new Date(expense.date).toLocaleDateString() : 'N/A'}
                  </div>
                )}
              </td>
              <td className="px-6 py-4">
                {editingId === expense.id ? (
                  <input 
                    className="input-field py-1"
                    value={editData.category}
                    onChange={(e) => setEditData({...editData, category: e.target.value})}
                  />
                ) : (
                  <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-primary-50 text-primary-700 uppercase">
                    <Tag className="w-3 h-3" />
                    {expense.category}
                  </span>
                )}
              </td>
              <td className="px-6 py-4 text-right">
                <div className="flex justify-end gap-2">
                  {editingId === expense.id ? (
                    <>
                      <button onClick={() => handleUpdate(expense.id)} className="p-2 text-green-600 hover:bg-green-50 rounded-lg">
                        <Check className="w-5 h-5" />
                      </button>
                      <button onClick={() => setEditingId(null)} className="p-2 text-gray-400 hover:bg-gray-50 rounded-lg">
                        <X className="w-5 h-5" />
                      </button>
                    </>
                  ) : (
                    <>
                      <button onClick={() => startEditing(expense)} className="p-2 text-gray-400 hover:bg-primary-50 hover:text-primary-600 rounded-lg">
                        <Edit2 className="w-5 h-5" />
                      </button>
                      <button onClick={() => handleDelete(expense.id)} className="p-2 text-gray-400 hover:bg-red-50 hover:text-red-600 rounded-lg">
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </>
                  )}
                </div>
              </td>
            </tr>
          ))}
          {expenses.length === 0 && (
            <tr>
              <td colSpan="5" className="px-6 py-12 text-center text-gray-500">
                No expenses found. Start by uploading a receipt!
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
