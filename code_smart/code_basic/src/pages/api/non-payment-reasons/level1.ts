import type { NextApiRequest, NextApiResponse } from 'next';
import { NonPaymentReason } from '@/types/nonPaymentReason';

// Mock level 1 reasons - replace with actual database queries
const mockLevel1Reasons: NonPaymentReason[] = [
  {
    id: 'customer-not-present',
    name: 'Khách hàng không có mặt',
    level: 1,
    isActive: true
  },
  {
    id: 'customer-refuses',
    name: 'Khách hàng từ chối thanh toán',
    level: 1,
    isActive: true
  },
  {
    id: 'technical-issue',
    name: 'Vấn đề kỹ thuật',
    level: 1,
    isActive: true
  },
  {
    id: 'system-error',
    name: 'Lỗi hệ thống',
    level: 1,
    isActive: true
  },
  {
    id: 'other',
    name: 'Khác',
    level: 1,
    isActive: true
  }
];

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<NonPaymentReason[] | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // In real implementation:
    // 1. Query master data from database
    // 2. Filter by isActive = true
    // 3. Apply caching (Redis/memory cache)
    // 4. Sort by display order
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 100));
    
    const activeReasons = mockLevel1Reasons.filter(reason => reason.isActive);
    
    res.status(200).json(activeReasons);
  } catch (error) {
    console.error('Error fetching level 1 reasons:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}