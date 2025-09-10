import type { NextApiRequest, NextApiResponse } from 'next';
import { NonPaymentReasonFormData, ValidationError, CareSystemMapping } from '@/types/nonPaymentReason';
import { nonPaymentValidator } from '@/utils/nonPaymentValidation';
import { CARE_SYSTEM_DEFAULTS } from '@/constants/nonPaymentReason';
import { format } from 'date-fns';

interface SubmitRequest extends NonPaymentReasonFormData {
  staffAccount: string;
}

interface SubmitResponse {
  success: boolean;
  message: string;
  errors?: ValidationError[];
}

// Mock user data - replace with actual user service
const mockUsers = {
  'staff001': {
    account: 'staff001',
    name: 'Nguyễn Văn A',
    role: 'debt_collector' as const,
    permissions: ['update_non_payment_reason', 'view_history']
  },
  'staff002': {
    account: 'staff002', 
    name: 'Trần Thị B',
    role: 'other' as const,
    permissions: ['update_non_payment_reason']
  }
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<SubmitResponse>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ 
      success: false, 
      message: 'Method not allowed' 
    });
  }

  try {
    const requestData: SubmitRequest = req.body;
    const { staffAccount, ...formData } = requestData;

    // Get user info
    const currentUser = mockUsers[staffAccount as keyof typeof mockUsers];
    if (!currentUser) {
      return res.status(401).json({
        success: false,
        message: 'Unauthorized user'
      });
    }

    // Server-side validation
    const validationErrors = nonPaymentValidator.validateForm(formData, currentUser);
    
    if (validationErrors.length > 0) {
      return res.status(400).json({
        success: false,
        message: 'Validation failed',
        errors: validationErrors
      });
    }

    // Process business logic
    const result = await processNonPaymentReason(formData, currentUser);
    
    if (!result.success) {
      return res.status(400).json(result);
    }

    res.status(200).json({
      success: true,
      message: 'Cập nhật thành công'
    });

  } catch (error) {
    console.error('Error processing non-payment reason:', error);
    res.status(500).json({
      success: false,
      message: 'Internal server error'
    });
  }
}

async function processNonPaymentReason(
  formData: NonPaymentReasonFormData,
  currentUser: any
): Promise<SubmitResponse> {
  try {
    // 1. Save to debt management database
    const debtManagementResult = await saveToDebtManagement(formData, currentUser);
    if (!debtManagementResult.success) {
      return debtManagementResult;
    }

    // 2. Save to customer management database  
    const customerManagementResult = await saveToCustomerManagement(formData, currentUser);
    if (!customerManagementResult.success) {
      return customerManagementResult;
    }

    // 3. Save to care system with field mapping
    const careSystemResult = await saveToCareSystem(formData, currentUser);
    if (!careSystemResult.success) {
      return careSystemResult;
    }

    return {
      success: true,
      message: 'Cập nhật thành công tất cả hệ thống'
    };

  } catch (error) {
    console.error('Error in processNonPaymentReason:', error);
    return {
      success: false,
      message: 'Có lỗi xảy ra khi xử lý'
    };
  }
}

// Mock database save functions - replace with actual implementations

async function saveToDebtManagement(
  formData: NonPaymentReasonFormData, 
  currentUser: any
): Promise<SubmitResponse> {
  // Simulate database save
  console.log('Saving to Debt Management DB:', {
    contractId: 'CONTRACT_001', // In real app, get from context
    staffAccount: currentUser.account,
    reasonLevel1: formData.reasonLevel1,
    reasonLevel2: formData.reasonLevel2,
    reasonLevel3: formData.reasonLevel3,
    note: formData.note,
    appointmentDate: formData.appointmentDate,
    appointmentTime: formData.appointmentTime,
    lockDate: formData.lockDate,
    createdAt: new Date()
  });

  // Simulate delay
  await new Promise(resolve => setTimeout(resolve, 100));
  
  return { success: true, message: 'Saved to debt management' };
}

async function saveToCustomerManagement(
  formData: NonPaymentReasonFormData,
  currentUser: any
): Promise<SubmitResponse> {
  // Simulate customer interaction log save
  console.log('Saving to Customer Management DB:', {
    contractId: 'CONTRACT_001',
    staffAccount: currentUser.account,
    interactionType: 'non_payment_reason_update',
    interactionDate: new Date(),
    details: {
      reasons: [formData.reasonLevel1, formData.reasonLevel2, formData.reasonLevel3].filter(Boolean),
      note: formData.note,
      nextAppointment: formData.appointmentDate
    }
  });

  await new Promise(resolve => setTimeout(resolve, 100));
  
  return { success: true, message: 'Saved to customer management' };
}

async function saveToCareSystem(
  formData: NonPaymentReasonFormData,
  currentUser: any
): Promise<SubmitResponse> {
  // Map fields according to business requirements
  const careSystemData: CareSystemMapping = {
    personContact: CARE_SYSTEM_DEFAULTS.PERSON_CONTACT, // Empty
    paymentCapability: CARE_SYSTEM_DEFAULTS.PAYMENT_CAPABILITY, // Empty
    task: CARE_SYSTEM_DEFAULTS.TASK, // Empty
    contactChannel: CARE_SYSTEM_DEFAULTS.CONTACT_CHANNEL, // 'MobiX'
    appointmentSchedule: `${format(formData.appointmentDate, 'dd/MM/yyyy')} ${formData.appointmentTime}`,
    lockDate: formData.lockDate ? format(formData.lockDate, 'dd/MM/yyyy') : '',
    lockStatus: formData.lockStatus || '',
    careNote: formData.note
  };

  console.log('Saving to Care System:', {
    contractId: 'CONTRACT_001',
    staffAccount: currentUser.account,
    careRecord: careSystemData,
    createdAt: new Date()
  });

  await new Promise(resolve => setTimeout(resolve, 100));
  
  return { success: true, message: 'Saved to care system' };
}