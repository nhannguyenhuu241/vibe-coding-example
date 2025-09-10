import type { NextApiRequest, NextApiResponse } from 'next';
import { NonPaymentHistory } from '@/types/nonPaymentReason';
import { startOfMonth, endOfMonth } from 'date-fns';

// Mock history data - replace with actual database queries
const mockHistory: NonPaymentHistory[] = [
  {
    id: '1',
    contractId: 'CONTRACT_001',
    createdDate: new Date('2024-01-15T10:30:00'),
    staffAccount: 'staff001',
    staffName: 'Nguyễn Văn A',
    reasonLevel1: 'Khách hàng không có mặt',
    reasonLevel2: 'Đi công tác',
    reasonLevel3: undefined,
    note: 'Khách hàng đi công tác 1 tuần, sẽ về vào cuối tuần',
    appointmentDate: new Date('2024-01-22T09:00:00'),
    lockDate: new Date('2024-01-25T00:00:00'),
    lockStatus: 'Duy trì'
  },
  {
    id: '2',
    contractId: 'CONTRACT_001',
    createdDate: new Date('2024-01-10T14:20:00'),
    staffAccount: 'staff002',
    staffName: 'Trần Thị B',
    reasonLevel1: 'Khách hàng từ chối thanh toán',
    reasonLevel2: 'Khó khăn tài chính',
    reasonLevel3: 'Mất việc làm',
    note: 'Khách hàng vừa mất việc, cam kết thanh toán trong tuần tới',
    appointmentDate: new Date('2024-01-17T10:00:00'),
    lockDate: undefined,
    lockStatus: undefined
  },
  {
    id: '3',
    contractId: 'CONTRACT_001',
    createdDate: new Date('2024-01-05T16:45:00'),
    staffAccount: 'staff001',
    staffName: 'Nguyễn Văn A',
    reasonLevel1: 'Vấn đề kỹ thuật',
    reasonLevel2: 'Sự cố mạng',
    reasonLevel3: 'Đứt cáp',
    note: 'Cáp bị đứt do thi công đường, đã liên hệ kỹ thuật khắc phục',
    appointmentDate: new Date('2024-01-08T08:00:00'),
    lockDate: undefined,
    lockStatus: undefined
  }
];

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<NonPaymentHistory[] | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { contractId } = req.query;

  if (!contractId || typeof contractId !== 'string') {
    return res.status(400).json({ error: 'Contract ID is required' });
  }

  try {
    // Filter history for current month and contract
    const currentMonth = new Date();
    const monthStart = startOfMonth(currentMonth);
    const monthEnd = endOfMonth(currentMonth);

    const filteredHistory = mockHistory
      .filter(record => 
        record.contractId === contractId &&
        record.createdDate >= monthStart &&
        record.createdDate <= monthEnd
      )
      .sort((a, b) => b.createdDate.getTime() - a.createdDate.getTime()); // Most recent first

    // In real implementation:
    // 1. Query database with contractId and date range
    // 2. Join with staff table to get staff names
    // 3. Include appointment dates from debt management tool
    // 4. Include lock dates from care system
    // 5. Apply proper pagination

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 200));
    
    res.status(200).json(filteredHistory);
  } catch (error) {
    console.error('Error fetching non-payment history:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}