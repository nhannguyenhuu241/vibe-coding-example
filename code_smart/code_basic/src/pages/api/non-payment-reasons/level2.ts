import type { NextApiRequest, NextApiResponse } from 'next';
import { NonPaymentReason } from '@/types/nonPaymentReason';

// Mock data - replace with actual database queries
const mockLevel2Reasons: Record<string, NonPaymentReason[]> = {
  'customer-not-present': [
    {
      id: 'business-trip',
      name: 'Đi công tác',
      level: 2,
      parentId: 'customer-not-present',
      isActive: true
    },
    {
      id: 'hospitalization',
      name: 'Nằm viện',
      level: 2,
      parentId: 'customer-not-present',
      isActive: true
    },
    {
      id: 'out-of-town',
      name: 'Về quê',
      level: 2,
      parentId: 'customer-not-present',
      isActive: true
    }
  ],
  'customer-refuses': [
    {
      id: 'financial-difficulty',
      name: 'Khó khăn tài chính',
      level: 2,
      parentId: 'customer-refuses',
      isActive: true
    },
    {
      id: 'service-dispute',
      name: 'Tranh chấp dịch vụ',
      level: 2,
      parentId: 'customer-refuses',
      isActive: true
    },
    {
      id: 'bill-dispute',
      name: 'Không đồng ý với hóa đơn',
      level: 2,
      parentId: 'customer-refuses',
      isActive: true
    }
  ],
  'technical-issue': [
    {
      id: 'network-problem',
      name: 'Sự cố mạng',
      level: 2,
      parentId: 'technical-issue',
      isActive: true
    },
    {
      id: 'equipment-failure',
      name: 'Hỏng thiết bị',
      level: 2,
      parentId: 'technical-issue',
      isActive: true
    }
  ],
  'system-error': [
    {
      id: 'payment-gateway-error',
      name: 'Lỗi cổng thanh toán',
      level: 2,
      parentId: 'system-error',
      isActive: true
    },
    {
      id: 'billing-system-error',
      name: 'Lỗi hệ thống cước',
      level: 2,
      parentId: 'system-error',
      isActive: true
    }
  ],
  'other': [
    {
      id: 'other-reason',
      name: 'Lý do khác',
      level: 2,
      parentId: 'other',
      isActive: true
    }
  ]
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<NonPaymentReason[] | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { level1 } = req.query;

  if (!level1 || typeof level1 !== 'string') {
    return res.status(400).json({ error: 'Level 1 ID is required' });
  }

  try {
    // In real implementation, query database based on level1 ID
    const reasons = mockLevel2Reasons[level1] || [];
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    res.status(200).json(reasons);
  } catch (error) {
    console.error('Error fetching level 2 reasons:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}