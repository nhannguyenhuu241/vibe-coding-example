import React, { useState, useEffect } from 'react';
import { useNonPaymentReasonStore } from '@/store/nonPaymentReasonStore';
import { nonPaymentValidator } from '@/utils/nonPaymentValidation';
import { FIELD_LABELS } from '@/constants/nonPaymentReason';
import { format } from 'date-fns';
import { ArrowLeftIcon } from '@heroicons/react/24/outline';
import toast from 'react-hot-toast';

interface NonPaymentReasonFormProps {
  contractId: string;
  onBack: () => void;
}

export const NonPaymentReasonForm: React.FC<NonPaymentReasonFormProps> = ({
  contractId,
  onBack
}) => {
  const {
    reasons,
    formData,
    errors,
    isLoading,
    currentUser,
    updateFormData,
    loadReasonsLevel2,
    loadReasonsLevel3,
    setErrors,
    submitForm,
    loadHistory
  } = useNonPaymentReasonStore();

  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    // Load initial data
    loadHistory(contractId);
  }, [contractId, loadHistory]);

  const handleReasonLevel1Change = async (value: string) => {
    updateFormData({ 
      reasonLevel1: value, 
      reasonLevel2: '', 
      reasonLevel3: '' 
    });
    
    if (value) {
      await loadReasonsLevel2(value);
    }
  };

  const handleReasonLevel2Change = async (value: string) => {
    updateFormData({ 
      reasonLevel2: value, 
      reasonLevel3: '' 
    });
    
    if (value && formData.reasonLevel1) {
      await loadReasonsLevel3(formData.reasonLevel1, value);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Client-side validation
    const validationErrors = nonPaymentValidator.validateForm(formData, currentUser);
    
    // Check if level 3 is required
    if (reasons.level3.length > 0 && !formData.reasonLevel3) {
      validationErrors.push({
        field: 'reasonLevel3',
        message: `Vui lòng nhập đầy đủ thông tin - ${FIELD_LABELS.reasonLevel3}`
      });
    }
    
    if (validationErrors.length > 0) {
      setErrors(validationErrors);
      toast.error('Vui lòng kiểm tra lại thông tin');
      return;
    }
    
    const success = await submitForm();
    
    if (success) {
      toast.success('Cập nhật thành công');
    } else {
      toast.error('Cập nhật thất bại');
    }
  };

  const getFieldError = (fieldName: string) => {
    return errors.find(error => error.field === fieldName)?.message;
  };

  const isDebtCollector = currentUser?.role === 'debt_collector';

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="px-4 py-4 flex items-center">
          <button
            onClick={onBack}
            className="flex items-center text-gray-600 hover:text-gray-900"
          >
            <ArrowLeftIcon className="h-5 w-5 mr-2" />
            Trả lý do không thanh toán
          </button>
        </div>
      </div>

      <div className="p-4 max-w-md mx-auto">
        <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm border">
          <div className="p-4 space-y-4">
            {/* Reason Level 1 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {FIELD_LABELS.reasonLevel1} *
              </label>
              <select
                value={formData.reasonLevel1}
                onChange={(e) => handleReasonLevel1Change(e.target.value)}
                className={`w-full p-3 border rounded-md ${
                  getFieldError('reasonLevel1') ? 'border-red-500' : 'border-gray-300'
                } focus:outline-none focus:ring-2 focus:ring-blue-500`}
                disabled={isLoading}
              >
                <option value="">Chọn nguyên nhân cấp 1</option>
                {reasons.level1.map((reason) => (
                  <option key={reason.id} value={reason.id}>
                    {reason.name}
                  </option>
                ))}
              </select>
              {getFieldError('reasonLevel1') && (
                <p className="text-red-500 text-xs mt-1">{getFieldError('reasonLevel1')}</p>
              )}
            </div>

            {/* Reason Level 2 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {FIELD_LABELS.reasonLevel2} *
              </label>
              <select
                value={formData.reasonLevel2}
                onChange={(e) => handleReasonLevel2Change(e.target.value)}
                className={`w-full p-3 border rounded-md ${
                  getFieldError('reasonLevel2') ? 'border-red-500' : 'border-gray-300'
                } focus:outline-none focus:ring-2 focus:ring-blue-500`}
                disabled={isLoading || !formData.reasonLevel1}
              >
                <option value="">Chọn nguyên nhân cấp 2</option>
                {reasons.level2.map((reason) => (
                  <option key={reason.id} value={reason.id}>
                    {reason.name}
                  </option>
                ))}
              </select>
              {getFieldError('reasonLevel2') && (
                <p className="text-red-500 text-xs mt-1">{getFieldError('reasonLevel2')}</p>
              )}
            </div>

            {/* Reason Level 3 - Conditional */}
            {reasons.level3.length > 0 && (
              <div className="animate-fade-in">
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  {FIELD_LABELS.reasonLevel3} *
                </label>
                <select
                  value={formData.reasonLevel3 || ''}
                  onChange={(e) => updateFormData({ reasonLevel3: e.target.value })}
                  className={`w-full p-3 border rounded-md ${
                    getFieldError('reasonLevel3') ? 'border-red-500' : 'border-gray-300'
                  } focus:outline-none focus:ring-2 focus:ring-blue-500`}
                  disabled={isLoading}
                >
                  <option value="">Chọn nguyên nhân cấp 3</option>
                  {reasons.level3.map((reason) => (
                    <option key={reason.id} value={reason.id}>
                      {reason.name}
                    </option>
                  ))}
                </select>
                {getFieldError('reasonLevel3') && (
                  <p className="text-red-500 text-xs mt-1">{getFieldError('reasonLevel3')}</p>
                )}
              </div>
            )}

            {/* Note */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {FIELD_LABELS.note} *
              </label>
              <textarea
                value={formData.note}
                onChange={(e) => updateFormData({ note: e.target.value })}
                placeholder="Nhập ghi chú chi tiết lý do không thanh toán..."
                className={`w-full p-3 border rounded-md h-24 resize-none ${
                  getFieldError('note') ? 'border-red-500' : 'border-gray-300'
                } focus:outline-none focus:ring-2 focus:ring-blue-500`}
                maxLength={500}
                disabled={isLoading}
              />
              <div className="flex justify-between items-center mt-1">
                {getFieldError('note') && (
                  <p className="text-red-500 text-xs">{getFieldError('note')}</p>
                )}
                <p className="text-gray-400 text-xs ml-auto">
                  {formData.note.length}/500
                </p>
              </div>
            </div>

            {/* Appointment Date & Time */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                {FIELD_LABELS.appointmentDate} *
              </label>
              <div className="flex space-x-2">
                <input
                  type="date"
                  value={format(formData.appointmentDate, 'yyyy-MM-dd')}
                  onChange={(e) => updateFormData({ appointmentDate: new Date(e.target.value) })}
                  className={`flex-1 p-3 border rounded-md ${
                    getFieldError('appointmentDate') ? 'border-red-500' : 'border-gray-300'
                  } focus:outline-none focus:ring-2 focus:ring-blue-500`}
                  disabled={isLoading}
                />
                <input
                  type="time"
                  value={formData.appointmentTime}
                  onChange={(e) => updateFormData({ appointmentTime: e.target.value })}
                  className="px-3 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  disabled={isLoading}
                />
              </div>
              {getFieldError('appointmentDate') && (
                <p className="text-red-500 text-xs mt-1">{getFieldError('appointmentDate')}</p>
              )}
            </div>

            {/* Lock Date - Only for Debt Collectors */}
            {isDebtCollector && (
              <LockDateSection 
                formData={formData}
                updateFormData={updateFormData}
                isLoading={isLoading}
                fieldError={getFieldError('lockDate')}
              />
            )}
          </div>

          {/* History Toggle */}
          <div className="px-4 py-2 border-t border-gray-100">
            <button
              type="button"
              onClick={() => setShowHistory(!showHistory)}
              className="flex items-center text-sm text-blue-600 hover:text-blue-800"
            >
              Lịch sử cập nhật
              <span className="ml-1 transform transition-transform">
                {showHistory ? '▲' : '▼'}
              </span>
            </button>
          </div>

          {/* History Section */}
          {showHistory && (
            <HistorySection />
          )}

          {/* Submit Button */}
          <div className="p-4 border-t border-gray-100">
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
            >
              {isLoading ? 'Đang xử lý...' : 'Cập nhật'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Lock Date Section Component
interface LockDateSectionProps {
  formData: any;
  updateFormData: (data: any) => void;
  isLoading: boolean;
  fieldError?: string;
}

const LockDateSection: React.FC<LockDateSectionProps> = ({
  formData,
  updateFormData,
  isLoading,
  fieldError
}) => {
  return (
    <div className="space-y-3 p-3 bg-gray-50 rounded-md">
      <label className="block text-sm font-medium text-gray-700">
        Ngày dự kiến khóa cước
      </label>
      
      {/* Frame 1: Lock Options */}
      <div>
        <select
          value={formData.lockOption}
          onChange={(e) => updateFormData({ 
            lockOption: e.target.value,
            lockDate: e.target.value === 'none' ? undefined : formData.lockDate
          })}
          className="w-full p-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isLoading}
        >
          <option value="none">Không chọn</option>
          <option value="schedule">Mục 2: Khóa sau mục 1...</option>
          <option value="cancel">Hủy lịch khóa</option>
        </select>
      </div>

      {/* Frame 2: Date Selection */}
      {formData.lockOption === 'schedule' && (
        <div className="animate-fade-in">
          <input
            type="date"
            value={formData.lockDate ? format(formData.lockDate, 'yyyy-MM-dd') : ''}
            onChange={(e) => updateFormData({ lockDate: new Date(e.target.value) })}
            className={`w-full p-2 border rounded-md text-sm ${
              fieldError ? 'border-red-500' : 'border-gray-300'
            } focus:outline-none focus:ring-2 focus:ring-blue-500`}
            disabled={isLoading}
          />
          {fieldError && (
            <p className="text-red-500 text-xs mt-1">{fieldError}</p>
          )}
        </div>
      )}

      {/* Frame 3: Lock Status */}
      {formData.lockOption === 'schedule' && formData.lockDate && (
        <div className="animate-fade-in">
          <select
            value={formData.lockStatus}
            onChange={(e) => updateFormData({ lockStatus: e.target.value })}
            className="w-full p-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          >
            <option value="maintain">Duy trì</option>
            <option value="temporary">Tạm thời</option>
          </select>
        </div>
      )}
    </div>
  );
};

// History Section Component
const HistorySection: React.FC = () => {
  const { history } = useNonPaymentReasonStore();

  return (
    <div className="px-4 py-3 border-t border-gray-100 bg-gray-50">
      <h4 className="text-sm font-medium text-gray-700 mb-3">Lịch sử trong tháng</h4>
      {history.length === 0 ? (
        <p className="text-sm text-gray-500">Chưa có lịch sử cập nhật</p>
      ) : (
        <div className="space-y-2 max-h-40 overflow-y-auto">
          {history.map((record) => (
            <div key={record.id} className="bg-white p-2 rounded text-xs border">
              <div className="flex justify-between items-start mb-1">
                <span className="font-medium text-gray-700">
                  {format(record.createdDate, 'dd/MM/yyyy HH:mm')}
                </span>
                <span className="text-gray-500">{record.staffName}</span>
              </div>
              <p className="text-gray-600 mb-1">
                {record.reasonLevel1} → {record.reasonLevel2}
                {record.reasonLevel3 && ` → ${record.reasonLevel3}`}
              </p>
              <p className="text-gray-500">{record.note}</p>
              {record.appointmentDate && (
                <p className="text-blue-600 mt-1">
                  Hẹn: {format(record.appointmentDate, 'dd/MM/yyyy HH:mm')}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};