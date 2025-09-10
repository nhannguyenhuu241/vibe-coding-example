import { NonPaymentReasonFormData, ValidationError, UserRole } from '@/types/nonPaymentReason';
import { VALIDATION_MESSAGES, FORM_CONSTRAINTS } from '@/constants/nonPaymentReason';
import { format, isAfter, startOfDay, endOfMonth, getDate } from 'date-fns';

export class NonPaymentValidator {
  private errors: ValidationError[] = [];

  validateForm(data: NonPaymentReasonFormData, currentUser: UserRole | null): ValidationError[] {
    this.errors = [];

    this.validateReasonLevel1(data.reasonLevel1);
    this.validateReasonLevel2(data.reasonLevel2);
    this.validateReasonLevel3(data.reasonLevel3);
    this.validateNote(data.note);
    this.validateAppointmentDate(data.appointmentDate);
    this.validateLockDate(data.lockDate, currentUser);

    return this.errors;
  }

  private validateReasonLevel1(value: string): void {
    if (!value?.trim()) {
      this.errors.push({
        field: 'reasonLevel1',
        message: `${VALIDATION_MESSAGES.REQUIRED_FIELD} - Nguyên nhân cấp 1`
      });
    }
  }

  private validateReasonLevel2(value: string): void {
    if (!value?.trim()) {
      this.errors.push({
        field: 'reasonLevel2',
        message: `${VALIDATION_MESSAGES.REQUIRED_FIELD} - Nguyên nhân cấp 2`
      });
    }
  }

  private validateReasonLevel3(value?: string): void {
    // Level 3 is conditionally required - validation handled in component
  }

  private validateNote(value: string): void {
    if (!value?.trim()) {
      this.errors.push({
        field: 'note',
        message: `${VALIDATION_MESSAGES.REQUIRED_FIELD} - Ghi chú`
      });
    } else if (value.length > FORM_CONSTRAINTS.MAX_NOTE_LENGTH) {
      this.errors.push({
        field: 'note',
        message: VALIDATION_MESSAGES.MAX_NOTE_LENGTH
      });
    }
  }

  private validateAppointmentDate(value: Date): void {
    if (!value) {
      this.errors.push({
        field: 'appointmentDate',
        message: `${VALIDATION_MESSAGES.REQUIRED_FIELD} - Ngày hẹn thanh toán`
      });
    } else {
      const today = startOfDay(new Date());
      const appointmentDay = startOfDay(value);
      
      if (!isAfter(appointmentDay, today) && appointmentDay.getTime() !== today.getTime()) {
        this.errors.push({
          field: 'appointmentDate',
          message: VALIDATION_MESSAGES.INVALID_DATE
        });
      }
    }
  }

  private validateLockDate(value?: Date, currentUser?: UserRole | null): void {
    if (!currentUser || currentUser.role !== 'debt_collector') {
      return;
    }

    if (value) {
      const today = new Date();
      const lockDate = getDate(value);
      const monthEnd = endOfMonth(today);
      
      if (lockDate < FORM_CONSTRAINTS.MIN_LOCK_DATE || lockDate > getDate(monthEnd)) {
        this.errors.push({
          field: 'lockDate',
          message: VALIDATION_MESSAGES.LOCK_DATE_ERROR
        });
      } else if (!isAfter(startOfDay(value), startOfDay(today))) {
        this.errors.push({
          field: 'lockDate',
          message: VALIDATION_MESSAGES.LOCK_DATE_ERROR
        });
      }
    }
  }

  static validateLockDateRange(date: Date): boolean {
    const today = new Date();
    const lockDate = getDate(date);
    const monthEnd = endOfMonth(today);
    
    return lockDate >= FORM_CONSTRAINTS.MIN_LOCK_DATE && 
           lockDate <= getDate(monthEnd) && 
           isAfter(startOfDay(date), startOfDay(today));
  }
}

export const nonPaymentValidator = new NonPaymentValidator();