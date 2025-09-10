import { useEffect, useCallback } from 'react';
import { useNonPaymentReasonStore } from '@/store/nonPaymentReasonStore';
import { nonPaymentValidator } from '@/utils/nonPaymentValidation';
import { FIELD_LABELS } from '@/constants/nonPaymentReason';
import toast from 'react-hot-toast';

export const useNonPaymentReasonForm = (contractId: string) => {
  const {
    reasons,
    formData,
    errors,
    isLoading,
    currentUser,
    history,
    updateFormData,
    loadReasonsLevel2,
    loadReasonsLevel3,
    setErrors,
    clearErrors,
    submitForm,
    loadHistory,
    setLevel1Reasons
  } = useNonPaymentReasonStore();

  // Load initial data
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        // Load level 1 reasons
        const level1Response = await fetch('/api/non-payment-reasons/level1');
        const level1Reasons = await level1Response.json();
        setLevel1Reasons(level1Reasons);

        // Load history
        await loadHistory(contractId);
      } catch (error) {
        console.error('Error loading initial data:', error);
        toast.error('Có lỗi khi tải dữ liệu');
      }
    };

    loadInitialData();
  }, [contractId, loadHistory, setLevel1Reasons]);

  // Handle reason cascade loading
  const handleReasonLevel1Change = useCallback(async (value: string) => {
    updateFormData({ 
      reasonLevel1: value, 
      reasonLevel2: '', 
      reasonLevel3: '' 
    });
    
    clearErrors();
    
    if (value) {
      await loadReasonsLevel2(value);
    }
  }, [updateFormData, clearErrors, loadReasonsLevel2]);

  const handleReasonLevel2Change = useCallback(async (value: string) => {
    updateFormData({ 
      reasonLevel2: value, 
      reasonLevel3: '' 
    });
    
    clearErrors();
    
    if (value && formData.reasonLevel1) {
      await loadReasonsLevel3(formData.reasonLevel1, value);
    }
  }, [updateFormData, clearErrors, loadReasonsLevel3, formData.reasonLevel1]);

  const handleReasonLevel3Change = useCallback((value: string) => {
    updateFormData({ reasonLevel3: value });
    clearErrors();
  }, [updateFormData, clearErrors]);

  // Handle form field changes with validation
  const handleFieldChange = useCallback((field: string, value: any) => {
    updateFormData({ [field]: value });
    
    // Clear specific field error when user starts typing
    const fieldErrors = errors.filter(error => error.field !== field);
    if (fieldErrors.length !== errors.length) {
      setErrors(fieldErrors);
    }
  }, [updateFormData, errors, setErrors]);

  // Lock date option handling
  const handleLockOptionChange = useCallback((option: string) => {
    const updates: any = { lockOption: option };
    
    if (option === 'none') {
      updates.lockDate = undefined;
      updates.lockStatus = undefined;
    } else if (option === 'cancel') {
      updates.lockDate = undefined;
      updates.lockStatus = 'cancelled';
    }
    
    updateFormData(updates);
    clearErrors();
  }, [updateFormData, clearErrors]);

  // Form submission with validation
  const handleSubmit = useCallback(async (e: React.FormEvent) => {
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
      
      // Focus first error field
      const firstErrorField = document.querySelector(`[name="${validationErrors[0].field}"]`) as HTMLElement;
      if (firstErrorField) {
        firstErrorField.focus();
        firstErrorField.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      
      return false;
    }
    
    // Submit form
    const toastId = toast.loading('Đang cập nhật...');
    
    try {
      const success = await submitForm();
      
      if (success) {
        toast.success('Cập nhật thành công', { id: toastId });
        return true;
      } else {
        toast.error('Cập nhật thất bại', { id: toastId });
        return false;
      }
    } catch (error) {
      toast.error('Có lỗi xảy ra', { id: toastId });
      return false;
    }
  }, [formData, currentUser, reasons.level3.length, setErrors, submitForm]);

  // Get field error helper
  const getFieldError = useCallback((fieldName: string) => {
    return errors.find(error => error.field === fieldName)?.message;
  }, [errors]);

  // Check if field has error
  const hasFieldError = useCallback((fieldName: string) => {
    return errors.some(error => error.field === fieldName);
  }, [errors]);

  // Get field CSS classes based on state
  const getFieldClasses = useCallback((fieldName: string, baseClasses: string) => {
    const hasError = hasFieldError(fieldName);
    const errorClasses = hasError ? 'border-red-500 bg-red-50' : 'border-gray-300';
    const focusClasses = 'focus:outline-none focus:ring-2 focus:ring-blue-500';
    
    return `${baseClasses} ${errorClasses} ${focusClasses}`;
  }, [hasFieldError]);

  // Check user permissions
  const isDebtCollector = currentUser?.role === 'debt_collector';
  const canManageLockDate = isDebtCollector;

  return {
    // State
    reasons,
    formData,
    errors,
    isLoading,
    currentUser,
    history,
    
    // Computed
    isDebtCollector,
    canManageLockDate,
    
    // Actions
    handleReasonLevel1Change,
    handleReasonLevel2Change,
    handleReasonLevel3Change,
    handleFieldChange,
    handleLockOptionChange,
    handleSubmit,
    
    // Helpers
    getFieldError,
    hasFieldError,
    getFieldClasses,
    
    // Store actions
    updateFormData,
    clearErrors
  };
};