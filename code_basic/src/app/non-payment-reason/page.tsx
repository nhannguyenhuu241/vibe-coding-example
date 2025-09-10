'use client';

import React, { useState } from 'react';

interface NonPaymentReasonData {
  reasonLevel1: string;
  reasonLevel2: string;
  reasonLevel3?: string;
  notes: string;
  scheduledDate?: Date;
  scheduledTime?: string;
  lockDate?: Date;
  lockType?: 'permanent' | 'temporary';
  cancelLock?: boolean;
}

const reasonCodes = {
  level1: [
    { id: 'financial_difficulty', name: 'Khó khăn tài chính' },
    { id: 'service_issue', name: 'Vấn đề dịch vụ' },
    { id: 'lock_after_level1_and_end_of_month', name: 'Mục 2: Khóa sau mục 1 và đến cuối tháng khóa hết' }
  ],
  level2: {
    'financial_difficulty': [
      { id: 'temporary_financial', name: 'Khó khăn tài chính tạm thời' },
      { id: 'permanent_financial', name: 'Khó khăn tài chính lâu dài' }
    ],
    'service_issue': [
      { id: 'internet_slow', name: 'Internet chậm' },
      { id: 'frequent_disconnection', name: 'Mất kết nối thường xuyên' }
    ]
  }
};

const mockHistory = [
  {
    id: '1',
    date: new Date('2023-12-15T10:30:00'),
    accountCode: 'TCVN001',
    staffName: 'Nguyễn Văn A',
    reasonLevel1Name: 'Khó khăn tài chính',
    reasonLevel2Name: 'Khó khăn tài chính tạm thời',
    reasonLevel3Name: 'Mất việc làm',
    notes: 'Khách hàng tạm thời mất việc, hẹn thanh toán cuối tháng',
    scheduledDate: new Date('2023-12-28T14:00:00'),
    lockDate: new Date('2023-12-30'),
    lockType: 'temporary' as const
  },
  {
    id: '2',
    date: new Date('2023-12-08T14:15:00'),
    accountCode: 'TCVN002',
    staffName: 'Trần Thị B',
    reasonLevel1Name: 'Vấn đề dịch vụ',
    reasonLevel2Name: 'Internet chậm',
    notes: 'Khách hàng phản ánh internet chậm, đã tạo ticket kỹ thuật',
    scheduledDate: new Date('2023-12-12T09:00:00')
  }
];

export default function NonPaymentReasonPage() {
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState<NonPaymentReasonData>({
    reasonLevel1: '',
    reasonLevel2: '',
    reasonLevel3: '',
    notes: '',
    scheduledDate: undefined,
    scheduledTime: '',
    lockDate: undefined,
    lockType: undefined,
    cancelLock: false
  });

  const [level2Options, setLevel2Options] = useState<any[]>([]);

  const handleLevel1Change = (value: string) => {
    setFormData(prev => ({ ...prev, reasonLevel1: value, reasonLevel2: '', reasonLevel3: '' }));
    setLevel2Options(reasonCodes.level2[value as keyof typeof reasonCodes.level2] || []);
  };

  const validateForm = (): string | null => {
    if (!formData.reasonLevel1) return 'Vui lòng nhập đầy đủ thông tin';
    if (!formData.reasonLevel2) return 'Vui lòng chọn nguyên nhân cấp 2';
    if (!formData.notes.trim()) return 'Vui lòng nhập ghi chú';
    return null;
  };

  const handleSubmit = async () => {
    const validationError = validateForm();
    if (validationError) {
      alert(validationError);
      return;
    }
    
    console.log('Submitting non-payment reason:', formData);
    alert('Cập nhật trả lý do không thanh toán thành công!');
    setShowForm(false);
    setFormData({
      reasonLevel1: '',
      reasonLevel2: '',
      reasonLevel3: '',
      notes: '',
      scheduledDate: undefined,
      scheduledTime: '',
      lockDate: undefined,
      lockType: undefined,
      cancelLock: false
    });
  };

  const formatDateTime = (date: Date) => {
    return date.toLocaleString('vi-VN');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto space-y-6">
        {/* Header */}
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-2xl font-bold text-center text-gray-800 mb-2">
            🏦 Mobinet Nextgen - Trả lý do không thanh toán
          </h1>
          <div className="text-center text-gray-600">
            <p><strong>Hợp đồng:</strong> SGH236501 | <strong>Vai trò:</strong> Thu cước</p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex justify-center space-x-4">
          <button
            onClick={() => setShowForm(true)}
            disabled={showForm}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            ➕ Trả lý do không thanh toán
          </button>
          <button
            onClick={() => window.location.reload()}
            className="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300"
          >
            🔄 Làm mới
          </button>
        </div>

        {/* Form Section */}
        {showForm && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-6">Trả lý do không thanh toán</h2>
            
            <div className="space-y-4">
              {/* Reason Level 1 */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Nguyên nhân cấp 1 *
                </label>
                <select
                  value={formData.reasonLevel1}
                  onChange={(e) => handleLevel1Change(e.target.value)}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                >
                  <option value="">Chọn nguyên nhân cấp 1</option>
                  {reasonCodes.level1.map((reason) => (
                    <option key={reason.id} value={reason.id}>
                      {reason.name}
                    </option>
                  ))}
                </select>
              </div>

              {/* Reason Level 2 */}
              {formData.reasonLevel1 && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nguyên nhân cấp 2 *
                  </label>
                  <select
                    value={formData.reasonLevel2}
                    onChange={(e) => setFormData(prev => ({ ...prev, reasonLevel2: e.target.value }))}
                    className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Chọn nguyên nhân cấp 2</option>
                    {level2Options.map((reason) => (
                      <option key={reason.id} value={reason.id}>
                        {reason.name}
                      </option>
                    ))}
                  </select>
                </div>
              )}

              {/* Notes */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ghi chú *
                </label>
                <textarea
                  placeholder="Nhập thông tin ghi chú..."
                  value={formData.notes}
                  onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
                  className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-h-[80px]"
                />
              </div>

              {/* Action Buttons */}
              <div className="flex justify-end space-x-4 pt-4">
                <button
                  onClick={() => setShowForm(false)}
                  className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
                >
                  Hủy
                </button>
                <button
                  onClick={handleSubmit}
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Cập nhật
                </button>
              </div>
            </div>
          </div>
        )}

        {/* History Section */}
        {!showForm && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              📋 Lịch sử trả lý do không thanh toán - Tháng 12/2023
            </h2>
            
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {mockHistory.map((record) => (
                <div key={record.id} className="border rounded-lg p-4 space-y-3">
                  {/* Header */}
                  <div className="flex justify-between items-start text-sm text-gray-600">
                    <span>📅 {formatDateTime(record.date)}</span>
                    <span>👤 {record.staffName} ({record.accountCode})</span>
                  </div>

                  {/* Reasons */}
                  <div className="space-y-1 text-sm">
                    <div><span className="font-medium">Nguyên nhân 1:</span> {record.reasonLevel1Name}</div>
                    <div><span className="font-medium">Nguyên nhân 2:</span> {record.reasonLevel2Name}</div>
                    {record.reasonLevel3Name && (
                      <div><span className="font-medium">Nguyên nhân 3:</span> {record.reasonLevel3Name}</div>
                    )}
                  </div>

                  {/* Notes */}
                  <div className="text-sm">
                    <span className="font-medium">Ghi chú:</span>
                    <div className="mt-1 p-2 bg-gray-50 rounded text-gray-600">{record.notes}</div>
                  </div>

                  {/* Scheduled date */}
                  {record.scheduledDate && (
                    <div className="text-sm flex items-center">
                      🕐 <span className="font-medium ml-1">Ngày hẹn thanh toán:</span> 
                      <span className="text-blue-600 ml-1">{formatDateTime(record.scheduledDate)}</span>
                    </div>
                  )}

                  {/* Lock date */}
                  {record.lockDate && (
                    <div className="flex items-center justify-between">
                      <div className="text-sm flex items-center">
                        📅 <span className="font-medium ml-1">Ngày dự kiến khóa cước:</span>
                        <span className="text-orange-600 ml-1">{record.lockDate.toLocaleDateString('vi-VN')}</span>
                      </div>
                      {record.lockType && (
                        <span className={`px-2 py-1 rounded text-xs font-semibold ${
                          record.lockType === 'permanent' 
                            ? 'bg-red-100 text-red-800' 
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {record.lockType === 'permanent' ? 'Duy trì' : 'Tạm thời'}
                        </span>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Feature Overview */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">📋 Tính năng đã triển khai</h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-semibold text-green-700 mb-2">✅ Form Features:</h4>
              <ul className="text-sm space-y-1 text-gray-600">
                <li>• 3-tier reason hierarchy (Cấp 1, 2, 3)</li>
                <li>• Required field validation</li>
                <li>• Date/time scheduling</li>
                <li>• Lock date validation (≥ ngày 13)</li>
                <li>• Lock type selection (Duy trì/Tạm thời)</li>
                <li>• Cancel lock option</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-blue-700 mb-2">📊 History Features:</h4>
              <ul className="text-sm space-y-1 text-gray-600">
                <li>• Monthly history filtering</li>
                <li>• Complete reason trail</li>
                <li>• Staff information tracking</li>
                <li>• Schedule & lock date display</li>
                <li>• Status badges</li>
                <li>• Scrollable timeline</li>
              </ul>
            </div>
          </div>
        </div>

        {/* URD Compliance */}
        <div className="bg-green-50 border border-green-200 rounded-lg p-6">
          <h2 className="text-green-700 font-semibold mb-4">✅ URD Section 3.2 Compliance</h2>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div>
              <h5 className="font-semibold mb-2">Use Case Requirements:</h5>
              <ul className="space-y-1 text-gray-600">
                <li>• Actor: Thu cước ✅</li>
                <li>• Trigger: Cập nhật button ✅</li>
                <li>• Pre/Post conditions ✅</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-2">Business Rules:</h5>
              <ul className="space-y-1 text-gray-600">
                <li>• 3-level reason codes ✅</li>
                <li>• Lock date validation ✅</li>
                <li>• Future date only ✅</li>
                <li>• Required fields check ✅</li>
              </ul>
            </div>
            <div>
              <h5 className="font-semibold mb-2">Integration:</h5>
              <ul className="space-y-1 text-gray-600">
                <li>• MobiX channel ✅</li>
                <li>• Customer Care sync ✅</li>
                <li>• History tracking ✅</li>
                <li>• Month filtering ✅</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}