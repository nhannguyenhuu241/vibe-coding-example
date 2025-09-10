export const VALIDATION_MESSAGES = {
  REQUIRED_FIELD: 'Vui lòng nhập đầy đủ thông tin',
  INVALID_DATE: 'Không thể chọn ngày quá khứ',
  LOCK_DATE_ERROR: 'Thao tác thất bại. Chỉ cho phép cập nhật lịch khóa từ ngày 13 đến cuối tháng và không cho phép chọn ngày khóa nhỏ hơn hoặc bằng ngày hiện tại.',
  MAX_NOTE_LENGTH: 'Ghi chú không được vượt quá 500 ký tự'
} as const;

export const FIELD_LABELS = {
  reasonLevel1: 'Nguyên nhân cấp 1',
  reasonLevel2: 'Nguyên nhân cấp 2', 
  reasonLevel3: 'Nguyên nhân cấp 3',
  note: 'Ghi chú',
  appointmentDate: 'Ngày hẹn thanh toán',
  lockDate: 'Ngày dự kiến khóa cước'
} as const;

export const LOCK_OPTIONS = {
  NONE: 'none',
  SCHEDULE: 'schedule',
  CANCEL: 'cancel'
} as const;

export const LOCK_STATUS_OPTIONS = {
  MAINTAIN: 'maintain',
  TEMPORARY: 'temporary'
} as const;

export const USER_ROLES = {
  DEBT_COLLECTOR: 'debt_collector',
  OTHER: 'other'
} as const;

export const CARE_SYSTEM_DEFAULTS = {
  PERSON_CONTACT: '',
  PAYMENT_CAPABILITY: '',
  TASK: '',
  CONTACT_CHANNEL: 'MobiX'
} as const;

export const FORM_CONSTRAINTS = {
  MAX_NOTE_LENGTH: 500,
  MIN_LOCK_DATE: 13,
  HISTORY_PERIOD_MONTHS: 1
} as const;