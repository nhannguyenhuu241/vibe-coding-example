import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { CalendarIcon, ClockIcon, UserIcon, FileTextIcon } from 'lucide-react';
import { format } from 'date-fns';

interface NonPaymentReasonHistoryRecord {
  id: string;
  date: Date;
  accountCode: string;
  staffName: string;
  reasonLevel1: string;
  reasonLevel1Name: string;
  reasonLevel2: string;
  reasonLevel2Name: string;
  reasonLevel3?: string;
  reasonLevel3Name?: string;
  notes: string;
  scheduledDate?: Date;
  lockDate?: Date;
  lockType?: 'permanent' | 'temporary';
}

interface NonPaymentReasonHistoryProps {
  contractId: string;
  currentMonth?: Date;
}

const NonPaymentReasonHistory: React.FC<NonPaymentReasonHistoryProps> = ({
  contractId,
  currentMonth = new Date()
}) => {
  const [historyRecords, setHistoryRecords] = useState<NonPaymentReasonHistoryRecord[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchHistoryRecords();
  }, [contractId, currentMonth]);

  const fetchHistoryRecords = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Mock data - replace with actual API call
      const mockHistory: NonPaymentReasonHistoryRecord[] = [
        {
          id: '1',
          date: new Date('2023-12-15T10:30:00'),
          accountCode: 'TCVN001',
          staffName: 'Nguyễn Văn A',
          reasonLevel1: 'financial_difficulty',
          reasonLevel1Name: 'Khó khăn tài chính',
          reasonLevel2: 'temporary_financial',
          reasonLevel2Name: 'Khó khăn tài chính tạm thời',
          reasonLevel3: 'job_loss',
          reasonLevel3Name: 'Mất việc làm',
          notes: 'Khách hàng tạm thời mất việc, hẹn thanh toán cuối tháng',
          scheduledDate: new Date('2023-12-28T14:00:00'),
          lockDate: new Date('2023-12-30'),
          lockType: 'temporary'
        },
        {
          id: '2',
          date: new Date('2023-12-08T14:15:00'),
          accountCode: 'TCVN002',
          staffName: 'Trần Thị B',
          reasonLevel1: 'service_issue',
          reasonLevel1Name: 'Vấn đề dịch vụ',
          reasonLevel2: 'internet_slow',
          reasonLevel2Name: 'Internet chậm',
          notes: 'Khách hàng phản ánh internet chậm, đã tạo ticket kỹ thuật',
          scheduledDate: new Date('2023-12-12T09:00:00')
        }
      ];

      // Filter by current month
      const filteredHistory = mockHistory.filter(record => {
        const recordMonth = record.date.getMonth();
        const recordYear = record.date.getFullYear();
        return recordMonth === currentMonth.getMonth() && recordYear === currentMonth.getFullYear();
      });

      setHistoryRecords(filteredHistory);
    } catch (err) {
      setError('Không thể tải lịch sử trả lý do');
      console.error('Failed to fetch history:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDateTime = (date: Date) => {
    return format(date, 'dd/MM/yyyy HH:mm');
  };

  const formatDate = (date: Date) => {
    return format(date, 'dd/MM/yyyy');
  };

  const getLockTypeLabel = (type: 'permanent' | 'temporary') => {
    return type === 'permanent' ? 'Duy trì' : 'Tạm thời';
  };

  const getLockTypeBadgeVariant = (type: 'permanent' | 'temporary') => {
    return type === 'permanent' ? 'destructive' : 'secondary';
  };

  if (loading) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Lịch sử trả lý do không thanh toán</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
            <span className="ml-2">Đang tải...</span>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Lịch sử trả lý do không thanh toán</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-red-500">
            {error}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (historyRecords.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>
            Lịch sử trả lý do không thanh toán - Tháng {currentMonth.getMonth() + 1}/{currentMonth.getFullYear()}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="text-center py-8 text-gray-500">
            Không có lịch sử trả lý do trong tháng này
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <FileTextIcon className="h-5 w-5" />
          <span>
            Lịch sử trả lý do không thanh toán - Tháng {currentMonth.getMonth() + 1}/{currentMonth.getFullYear()}
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-96">
          <div className="space-y-4">
            {historyRecords.map((record) => (
              <div key={record.id} className="border rounded-lg p-4 space-y-3">
                {/* Header with date and staff info */}
                <div className="flex justify-between items-start">
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <CalendarIcon className="h-4 w-4" />
                    <span>{formatDateTime(record.date)}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-sm text-gray-600">
                    <UserIcon className="h-4 w-4" />
                    <span>{record.staffName} ({record.accountCode})</span>
                  </div>
                </div>

                {/* Reasons hierarchy */}
                <div className="space-y-2">
                  <div className="text-sm">
                    <span className="font-medium text-gray-700">Nguyên nhân 1:</span>
                    <span className="ml-2">{record.reasonLevel1Name}</span>
                  </div>
                  <div className="text-sm">
                    <span className="font-medium text-gray-700">Nguyên nhân 2:</span>
                    <span className="ml-2">{record.reasonLevel2Name}</span>
                  </div>
                  {record.reasonLevel3Name && (
                    <div className="text-sm">
                      <span className="font-medium text-gray-700">Nguyên nhân 3:</span>
                      <span className="ml-2">{record.reasonLevel3Name}</span>
                    </div>
                  )}
                </div>

                {/* Notes */}
                <div className="text-sm">
                  <span className="font-medium text-gray-700">Ghi chú:</span>
                  <p className="mt-1 text-gray-600 bg-gray-50 p-2 rounded">{record.notes}</p>
                </div>

                {/* Scheduled date */}
                {record.scheduledDate && (
                  <div className="flex items-center space-x-2 text-sm">
                    <ClockIcon className="h-4 w-4 text-blue-500" />
                    <span className="font-medium text-gray-700">Ngày hẹn thanh toán:</span>
                    <span className="text-blue-600">{formatDateTime(record.scheduledDate)}</span>
                  </div>
                )}

                {/* Lock date and type */}
                {record.lockDate && (
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2 text-sm">
                      <CalendarIcon className="h-4 w-4 text-orange-500" />
                      <span className="font-medium text-gray-700">Ngày dự kiến khóa cước:</span>
                      <span className="text-orange-600">{formatDate(record.lockDate)}</span>
                    </div>
                    {record.lockType && (
                      <Badge variant={getLockTypeBadgeVariant(record.lockType)}>
                        {getLockTypeLabel(record.lockType)}
                      </Badge>
                    )}
                  </div>
                )}

                {/* Divider for multiple records */}
                {historyRecords.indexOf(record) < historyRecords.length - 1 && (
                  <hr className="mt-4" />
                )}
              </div>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
};

export default NonPaymentReasonHistory;