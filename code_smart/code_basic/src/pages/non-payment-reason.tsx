import React, { useEffect, useState } from 'react';
import Head from 'next/head';
import { NonPaymentReasonForm } from '@/components/NonPaymentReasonForm';
import { useNonPaymentReasonStore } from '@/store/nonPaymentReasonStore';
import { UserRole } from '@/types/nonPaymentReason';

const NonPaymentReasonPage: React.FC = () => {
  const { setLevel1Reasons, setCurrentUser } = useNonPaymentReasonStore();
  const [showForm, setShowForm] = useState(false);
  const [selectedUser, setSelectedUser] = useState<'debt_collector' | 'other'>('debt_collector');

  // Mock users for demo
  const mockUsers: Record<string, UserRole> = {
    debt_collector: {
      account: 'staff001',
      name: 'Nguyễn Văn A (Thu cước)',
      role: 'debt_collector',
      permissions: ['update_non_payment_reason', 'view_history', 'manage_lock_date']
    },
    other: {
      account: 'staff002',
      name: 'Trần Thị B (Khác)',
      role: 'other',
      permissions: ['update_non_payment_reason', 'view_history']
    }
  };

  useEffect(() => {
    // Load initial level 1 reasons
    loadLevel1Reasons();
  }, []);

  const loadLevel1Reasons = async () => {
    try {
      const response = await fetch('/api/non-payment-reasons/level1');
      const reasons = await response.json();
      setLevel1Reasons(reasons);
    } catch (error) {
      console.error('Error loading level 1 reasons:', error);
    }
  };

  const handleUserSelect = (userType: 'debt_collector' | 'other') => {
    setSelectedUser(userType);
    setCurrentUser(mockUsers[userType]);
  };

  const handleStartDemo = () => {
    setCurrentUser(mockUsers[selectedUser]);
    setShowForm(true);
  };

  if (showForm) {
    return (
      <NonPaymentReasonForm 
        contractId="CONTRACT_001"
        onBack={() => setShowForm(false)}
      />
    );
  }

  return (
    <>
      <Head>
        <title>Non-Payment Reason Analysis - Mobinet Nextgen</title>
        <meta name="description" content="Module trả lý do không thanh toán" />
      </Head>

      <div className="min-h-screen bg-gray-50 py-8">
        <div className="max-w-md mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-2">
              Module Trả lý do không thanh toán
            </h1>
            <p className="text-gray-600">
              Non-Payment Reason Analysis Demo
            </p>
          </div>

          {/* Demo Setup */}
          <div className="bg-white rounded-lg shadow-sm border p-6 mb-6">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">
              Chọn người dùng để demo
            </h2>
            
            <div className="space-y-3 mb-6">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="userType"
                  value="debt_collector"
                  checked={selectedUser === 'debt_collector'}
                  onChange={(e) => handleUserSelect(e.target.value as 'debt_collector')}
                  className="mr-3"
                />
                <div>
                  <div className="font-medium text-gray-800">Thu cước</div>
                  <div className="text-sm text-gray-600">
                    Có quyền thiết lập ngày khóa cước
                  </div>
                </div>
              </label>

              <label className="flex items-center">
                <input
                  type="radio"
                  name="userType"
                  value="other"
                  checked={selectedUser === 'other'}
                  onChange={(e) => handleUserSelect(e.target.value as 'other')}
                  className="mr-3"
                />
                <div>
                  <div className="font-medium text-gray-800">Nhân viên khác</div>
                  <div className="text-sm text-gray-600">
                    Không có quyền thiết lập ngày khóa cước
                  </div>
                </div>
              </label>
            </div>

            <button
              onClick={handleStartDemo}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 font-medium"
            >
              Bắt đầu demo với {mockUsers[selectedUser].name}
            </button>
          </div>

          {/* Feature Overview */}
          <div className="bg-white rounded-lg shadow-sm border p-6">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Tính năng chính
            </h3>
            
            <ul className="space-y-3 text-sm text-gray-600">
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Cascade loading nguyên nhân 3 cấp độ
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Validation form theo business rules
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Thiết lập ngày hẹn thanh toán
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Quản lý lịch khóa cước (Thu cước only)
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Lịch sử cập nhật trong tháng
              </li>
              <li className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                Tích hợp hệ thống chăm sóc KH
              </li>
            </ul>
          </div>
        </div>
      </div>
    </>
  );
};

export default NonPaymentReasonPage;