// =============================================================================
// MOBINET NEXTGEN VER 2.0 - TYPE DEFINITIONS (WEB)
// =============================================================================

// User & Authentication Types
export interface User {
  id: string;
  employeeCode: string;
  name: string;
  role: UserRole;
  department: string;
  permissions: Permission[];
  avatar?: string;
  email?: string;
  phone?: string;
}

export enum UserRole {
  SALE = 'SALE',
  TIN_PNC = 'TIN_PNC', // Nhân viên kỹ thuật
  THU_CUOC = 'THU_CUOC', // Nhân viên thu cước
}

export interface Permission {
  module: string;
  actions: string[];
}

// Payment Types
export interface Bill {
  id: string;
  contractNumber: string;
  customerName: string;
  customerPhone: string;
  amount: number;
  dueDate: string;
  status: BillStatus;
  services: ServiceDetail[];
  type: BillType;
}

export enum BillStatus {
  PENDING = 'PENDING',
  PAID = 'PAID',
  OVERDUE = 'OVERDUE',
  CANCELLED = 'CANCELLED',
}

export enum BillType {
  NORMAL = 'NORMAL', // Hóa đơn bình thường
  COLLECTION = 'COLLECTION', // Khoản thu
}

export interface ServiceDetail {
  id: string;
  name: string;
  amount: number;
  period: string;
}

export interface Payment {
  id: string;
  billId: string;
  amount: number;
  method: PaymentMethod;
  status: PaymentStatus;
  createdAt: string;
  completedAt?: string;
  transactionId?: string;
  note?: string;
}

export enum PaymentMethod {
  CASH_TEMP = 'CASH_TEMP', // Tiền mặt tạm
  FPT_PAY = 'FPT_PAY', // Ví FPT Pay
  QR_VNPAY = 'QR_VNPAY', // QR Code VN Pay
}

export enum PaymentStatus {
  PENDING = 'PENDING',
  PROCESSING = 'PROCESSING',
  SUCCESS = 'SUCCESS',
  FAILED = 'FAILED',
  CANCELLED = 'CANCELLED',
}

// Payment Limit Types
export interface PaymentLimit {
  userId: string;
  dailyLimit: number;
  monthlyLimit: number;
  usedDaily: number;
  usedMonthly: number;
  hmbs?: number; // Hạn mức bổ sung
}

// Wallet & Banking Types
export interface WalletInfo {
  id: string;
  type: WalletType;
  name: string;
  accountNumber?: string;
  bankName?: string;
  isDefault: boolean;
  isActive: boolean;
}

export enum WalletType {
  FPT_PAY = 'FPT_PAY',
  BANK_ACCOUNT = 'BANK_ACCOUNT',
}

// Notification Types
export interface NotificationConfig {
  userId: string;
  hiFptEnabled: boolean;
  smsEnabled: boolean;
  znsEnabled: boolean;
  monthlySmsSent: number;
  maxMonthlySmS: number;
}

export interface NotificationMessage {
  id: string;
  recipient: string;
  channel: NotificationChannel;
  content: string;
  status: NotificationStatus;
  sentAt?: string;
}

export enum NotificationChannel {
  HI_FPT = 'HI_FPT',
  SMS = 'SMS',
  ZNS = 'ZNS',
}

export enum NotificationStatus {
  PENDING = 'PENDING',
  SENT = 'SENT',
  DELIVERED = 'DELIVERED',
  FAILED = 'FAILED',
}

// Representative Payment Types
export interface RepresentativeContract {
  contractNumber: string;
  customerName: string;
  customerPhone: string;
  bills: Bill[];
  totalAmount: number;
  selected: boolean;
}

// Non-Payment Reason Types
export interface NonPaymentReason {
  id: string;
  billId: string;
  reason: string;
  scheduledDate?: string;
  expectedLockDate?: string;
  note?: string;
  createdAt: string;
}

// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: string[];
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  hasNext: boolean;
  hasPrev: boolean;
}

// Form Types
export interface LoginForm {
  employeeCode: string;
  password: string;
  rememberMe?: boolean;
}

export interface PaymentForm {
  billIds: string[];
  method: PaymentMethod;
  amount: number;
  note?: string;
}

// Component Props Types
export interface BaseComponentProps {
  className?: string;
  children?: React.ReactNode;
}

// Error Types
export interface AppError {
  code: string;
  message: string;
  details?: any;
}

// Dashboard Types
export interface DashboardStats {
  totalBills: number;
  pendingPayments: number;
  todayRevenue: number;
  monthlyRevenue: number;
  paymentLimitUsage: number;
}

// Table Types
export interface TableColumn<T> {
  key: keyof T;
  label: string;
  sortable?: boolean;
  render?: (value: any, record: T) => React.ReactNode;
}

export interface TableProps<T> {
  data: T[];
  columns: TableColumn<T>[];
  loading?: boolean;
  pagination?: {
    current: number;
    pageSize: number;
    total: number;
    onChange: (page: number) => void;
  };
}

// Modal Types
export interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  children: React.ReactNode;
}

// Toast Types
export interface ToastOptions {
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message?: string;
  duration?: number;
}

