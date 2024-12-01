import React from 'react';

const transactions = [
  {
    company: 'Google',
    logo: 'G',
    client: 'Jeremy Rice',
    amount: 744,
    rating: 4.2,
    status: 'Good',
  },
  {
    company: 'Facebook',
    logo: 'F',
    client: 'Antonio Greene',
    amount: 900,
    rating: 4.6,
    status: 'Good',
  },
  {
    company: 'YouTube',
    logo: 'Y',
    client: 'Clarence Diaz',
    amount: 560,
    rating: 2.8,
    status: 'Bad',
  },
];

export default function TransactionsTable() {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold">Transactions</h3>
        <button className="text-gray-400 hover:text-gray-600">•••</button>
      </div>
      <table className="w-full">
        <thead>
          <tr className="text-left text-sm text-gray-500">
            <th className="pb-4">Company</th>
            <th className="pb-4">Client</th>
            <th className="pb-4">Amount</th>
            <th className="pb-4">Rating</th>
            <th className="pb-4">Status</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((transaction) => (
            <tr key={transaction.client} className="border-t">
              <td className="py-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center">
                    {transaction.logo}
                  </div>
                  <span>{transaction.company}</span>
                </div>
              </td>
              <td className="py-4">{transaction.client}</td>
              <td className="py-4">${transaction.amount}</td>
              <td className="py-4">{transaction.rating}</td>
              <td className="py-4">
                <span className={`px-2 py-1 rounded-full text-sm ${
                  transaction.status === 'Good' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
                }`}>
                  {transaction.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}