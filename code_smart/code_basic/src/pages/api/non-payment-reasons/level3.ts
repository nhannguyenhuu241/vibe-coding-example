import type { NextApiRequest, NextApiResponse } from 'next';
import { NonPaymentReason } from '@/types/nonPaymentReason';

// Mock data - some level 2 reasons have level 3, some don't
const mockLevel3Reasons: Record<string, NonPaymentReason[]> = {
  'financial-difficulty': [
    {
      id: 'job-loss',
      name: 'Mất việc làm',
      level: 3,
      parentId: 'financial-difficulty',
      isActive: true
    },
    {
      id: 'salary-delay',
      name: 'Chậm lương',
      level: 3,
      parentId: 'financial-difficulty',
      isActive: true
    },
    {
      id: 'family-emergency',
      name: 'Biến cố gia đình',
      level: 3,
      parentId: 'financial-difficulty',
      isActive: true
    }
  ],
  'service-dispute': [
    {
      id: 'speed-issue',
      name: 'Tốc độ chậm',
      level: 3,
      parentId: 'service-dispute',
      isActive: true
    },
    {
      id: 'frequent-disconnection',
      name: 'Hay bị ngắt kết nối',
      level: 3,
      parentId: 'service-dispute',
      isActive: true
    },
    {
      id: 'service-not-as-promised',
      name: 'Dịch vụ không như cam kết',
      level: 3,
      parentId: 'service-dispute',
      isActive: true
    }
  ],
  'network-problem': [
    {
      id: 'cable-cut',
      name: 'Đứt cáp',
      level: 3,
      parentId: 'network-problem',
      isActive: true
    },
    {
      id: 'maintenance',
      name: 'Bảo trì hệ thống',
      level: 3,
      parentId: 'network-problem',
      isActive: true
    }
  ]
  // Note: Other level2 reasons don't have level3 (business rule)
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<NonPaymentReason[] | { error: string }>
) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { level1, level2 } = req.query;

  if (!level1 || !level2 || typeof level1 !== 'string' || typeof level2 !== 'string') {
    return res.status(400).json({ error: 'Level 1 and Level 2 IDs are required' });
  }

  try {
    // In real implementation, query database based on level1 and level2 IDs
    // For now, we only use level2 to determine level3 reasons
    const reasons = mockLevel3Reasons[level2] || [];
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 200));
    
    res.status(200).json(reasons);
  } catch (error) {
    console.error('Error fetching level 3 reasons:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}