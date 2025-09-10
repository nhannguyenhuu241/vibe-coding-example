export interface NonPaymentReason {
  id: string;
  name: string;
  level: 1 | 2 | 3;
  parentId?: string;
  isActive: boolean;
}

export interface NonPaymentReasonFormData {
  reasonLevel1: string;
  reasonLevel2: string;
  reasonLevel3?: string;
  note: string;
  appointmentDate: Date;
  appointmentTime: string;
  lockDate?: Date;
  lockStatus?: 'maintain' | 'temporary';
  lockOption?: 'none' | 'schedule' | 'cancel';
}

export interface NonPaymentHistory {
  id: string;
  contractId: string;
  createdDate: Date;
  staffAccount: string;
  staffName: string;
  reasonLevel1: string;
  reasonLevel2: string;
  reasonLevel3?: string;
  note: string;
  appointmentDate: Date;
  lockDate?: Date;
  lockStatus?: string;
}

export interface ValidationError {
  field: string;
  message: string;
}

export interface LockDateFrame {
  id: number;
  title: string;
  visible: boolean;
  required: boolean;
}

export interface CareSystemMapping {
  personContact: string;
  paymentCapability: string;
  task: string;
  contactChannel: string;
  appointmentSchedule: string;
  lockDate: string;
  lockStatus: string;
  careNote: string;
}

export interface UserRole {
  account: string;
  name: string;
  role: 'debt_collector' | 'other';
  permissions: string[];
}

export interface NonPaymentReasonState {
  reasons: {
    level1: NonPaymentReason[];
    level2: NonPaymentReason[];
    level3: NonPaymentReason[];
  };
  formData: NonPaymentReasonFormData;
  history: NonPaymentHistory[];
  isLoading: boolean;
  errors: ValidationError[];
  currentUser: UserRole | null;
}