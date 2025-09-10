import { ApiResponse, apiClient } from './client';

export interface ReasonCode {
  id: string;
  code: string;
  name: string;
  level: 1 | 2 | 3;
  parentId?: string;
  active: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface NonPaymentReasonSubmission {
  contractId: string;
  reasonLevel1: string;
  reasonLevel2: string;
  reasonLevel3?: string;
  notes: string;
  scheduledDate?: Date;
  scheduledTime?: string;
  lockDate?: Date;
  lockType?: 'permanent' | 'temporary';
  cancelLock?: boolean;
  staffId: string;
  channel: 'MobiX';
}

export interface NonPaymentReasonRecord {
  id: string;
  contractId: string;
  submissionDate: Date;
  staffId: string;
  staffName: string;
  staffCode: string;
  reasonLevel1: string;
  reasonLevel1Name: string;
  reasonLevel2: string;
  reasonLevel2Name: string;
  reasonLevel3?: string;
  reasonLevel3Name?: string;
  notes: string;
  scheduledDate?: Date;
  scheduledTime?: string;
  lockDate?: Date;
  lockType?: 'permanent' | 'temporary';
  cancelLock: boolean;
  syncedToCustomerCare: boolean;
  syncedToDebtManagement: boolean;
  createdAt: Date;
  updatedAt: Date;
}

export interface NonPaymentReasonHistoryFilter {
  contractId: string;
  month: number;
  year: number;
}

class NonPaymentReasonAPI {
  private readonly basePath = '/non-payment-reasons';

  /**
   * Fetch all reason codes with optional parent filtering
   */
  async getReasonCodes(parentId?: string, level?: number): Promise<ApiResponse<ReasonCode[]>> {
    const params = new URLSearchParams();
    if (parentId) params.append('parentId', parentId);
    if (level) params.append('level', level.toString());
    
    return apiClient.get(`${this.basePath}/codes?${params.toString()}`);
  }

  /**
   * Get reason codes hierarchy for a specific level
   */
  async getReasonCodesByLevel(level: 1 | 2 | 3, parentId?: string): Promise<ApiResponse<ReasonCode[]>> {
    const params = new URLSearchParams();
    params.append('level', level.toString());
    if (parentId) params.append('parentId', parentId);
    
    return apiClient.get(`${this.basePath}/codes/by-level?${params.toString()}`);
  }

  /**
   * Submit a non-payment reason record
   */
  async submitNonPaymentReason(data: NonPaymentReasonSubmission): Promise<ApiResponse<NonPaymentReasonRecord>> {
    // Validate data before submission
    this.validateSubmission(data);
    
    return apiClient.post(`${this.basePath}/submit`, data);
  }

  /**
   * Get non-payment reason history for a contract
   */
  async getHistory(filter: NonPaymentReasonHistoryFilter): Promise<ApiResponse<NonPaymentReasonRecord[]>> {
    const params = new URLSearchParams();
    params.append('contractId', filter.contractId);
    params.append('month', filter.month.toString());
    params.append('year', filter.year.toString());
    
    return apiClient.get(`${this.basePath}/history?${params.toString()}`);
  }

  /**
   * Get latest non-payment reason record for a contract
   */
  async getLatestRecord(contractId: string): Promise<ApiResponse<NonPaymentReasonRecord | null>> {
    return apiClient.get(`${this.basePath}/latest/${contractId}`);
  }

  /**
   * Update scheduled payment date for existing record
   */
  async updateScheduledDate(
    recordId: string, 
    scheduledDate: Date, 
    scheduledTime?: string
  ): Promise<ApiResponse<NonPaymentReasonRecord>> {
    return apiClient.patch(`${this.basePath}/${recordId}/schedule`, {
      scheduledDate,
      scheduledTime
    });
  }

  /**
   * Update lock schedule for existing record
   */
  async updateLockSchedule(
    recordId: string,
    lockDate?: Date,
    lockType?: 'permanent' | 'temporary',
    cancelLock?: boolean
  ): Promise<ApiResponse<NonPaymentReasonRecord>> {
    // Validate lock schedule rules
    if (lockDate && !cancelLock) {
      this.validateLockDate(lockDate);
      if (!lockType) {
        throw new Error('Lock type is required when setting lock date');
      }
    }

    return apiClient.patch(`${this.basePath}/${recordId}/lock-schedule`, {
      lockDate,
      lockType,
      cancelLock
    });
  }

  /**
   * Sync data to external systems (Customer Care, Debt Management)
   */
  async syncToExternalSystems(recordId: string): Promise<ApiResponse<{ success: boolean; synced: string[] }>> {
    return apiClient.post(`${this.basePath}/${recordId}/sync`);
  }

  /**
   * Get sync status for a record
   */
  async getSyncStatus(recordId: string): Promise<ApiResponse<{ 
    customerCareSync: boolean; 
    debtManagementSync: boolean; 
    lastSyncAt?: Date 
  }>> {
    return apiClient.get(`${this.basePath}/${recordId}/sync-status`);
  }

  /**
   * Validate submission data
   */
  private validateSubmission(data: NonPaymentReasonSubmission): void {
    if (!data.contractId) {
      throw new Error('Contract ID is required');
    }
    if (!data.reasonLevel1) {
      throw new Error('Reason level 1 is required');
    }
    if (!data.reasonLevel2) {
      throw new Error('Reason level 2 is required');
    }
    if (!data.notes.trim()) {
      throw new Error('Notes are required');
    }
    if (!data.staffId) {
      throw new Error('Staff ID is required');
    }

    // Validate lock date if provided
    if (data.lockDate && !data.cancelLock) {
      this.validateLockDate(data.lockDate);
      if (!data.lockType) {
        throw new Error('Lock type is required when setting lock date');
      }
    }
  }

  /**
   * Validate lock date according to business rules
   */
  private validateLockDate(lockDate: Date): void {
    const today = new Date();
    const day = lockDate.getDate();
    
    // Rule: Only allow lock dates from 13th to end of month
    if (day < 13) {
      throw new Error('Chỉ cho phép cập nhật lịch khóa từ ngày 13 đến cuối tháng và không cho phép chọn ngày khóa nhỏ hơn hoặc bằng ngày hiện tại.');
    }
    
    // Rule: Lock date must be in the future
    if (lockDate <= today) {
      throw new Error('Chỉ cho phép cập nhật lịch khóa từ ngày 13 đến cuối tháng và không cho phép chọn ngày khóa nhỏ hơn hoặc bằng ngày hiện tại.');
    }
  }
}

// Export singleton instance
export const nonPaymentReasonAPI = new NonPaymentReasonAPI();

// Export types for external use
export type { NonPaymentReasonSubmission, NonPaymentReasonRecord, NonPaymentReasonHistoryFilter };