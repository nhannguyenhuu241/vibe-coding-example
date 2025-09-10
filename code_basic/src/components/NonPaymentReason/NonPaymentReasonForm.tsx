import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Calendar } from '@/components/ui/calendar';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
import { CalendarIcon, Clock } from 'lucide-react';
import { format } from 'date-fns';
import { cn } from '@/lib/utils';

interface ReasonCode {
  id: string;
  name: string;
  level: 1 | 2 | 3;
  parentId?: string;
}

interface NonPaymentReasonFormProps {
  contractId: string;
  onSubmit: (data: NonPaymentReasonData) => void;
  onCancel: () => void;
  isDebtCollection?: boolean;
}

interface NonPaymentReasonData {
  reasonLevel1: string;
  reasonLevel2: string;
  reasonLevel3?: string;
  notes: string;
  scheduledDate?: Date;
  scheduledTime?: string;
  lockDate?: Date;
  lockType?: 'permanent' | 'temporary';
  cancelLock?: boolean;
}

const NonPaymentReasonForm: React.FC<NonPaymentReasonFormProps> = ({
  contractId,
  onSubmit,
  onCancel,
  isDebtCollection = false
}) => {
  const [formData, setFormData] = useState<NonPaymentReasonData>({
    reasonLevel1: '',
    reasonLevel2: '',
    reasonLevel3: '',
    notes: '',
    scheduledDate: undefined,
    scheduledTime: '',
    lockDate: undefined,
    lockType: undefined,
    cancelLock: false
  });

  const [reasonCodes, setReasonCodes] = useState<ReasonCode[]>([]);
  const [level2Options, setLevel2Options] = useState<ReasonCode[]>([]);
  const [level3Options, setLevel3Options] = useState<ReasonCode[]>([]);
  const [showLevel3, setShowLevel3] = useState(false);
  const [showLockScheduling, setShowLockScheduling] = useState(false);

  // Load reason codes on component mount
  useEffect(() => {
    fetchReasonCodes();
  }, []);

  // Update level 2 options when level 1 changes
  useEffect(() => {
    if (formData.reasonLevel1) {
      const level2Reasons = reasonCodes.filter(
        reason => reason.level === 2 && reason.parentId === formData.reasonLevel1
      );
      setLevel2Options(level2Reasons);
      setFormData(prev => ({ ...prev, reasonLevel2: '', reasonLevel3: '' }));
      setShowLevel3(false);
    }
  }, [formData.reasonLevel1, reasonCodes]);

  // Update level 3 options when level 2 changes
  useEffect(() => {
    if (formData.reasonLevel2) {
      const level3Reasons = reasonCodes.filter(
        reason => reason.level === 3 && reason.parentId === formData.reasonLevel2
      );
      setLevel3Options(level3Reasons);
      setShowLevel3(level3Reasons.length > 0);
      setFormData(prev => ({ ...prev, reasonLevel3: '' }));
    }
  }, [formData.reasonLevel2, reasonCodes]);

  // Check if lock scheduling should be shown
  useEffect(() => {
    const shouldShowLock = formData.reasonLevel1 === 'lock_after_level1_and_end_of_month';
    setShowLockScheduling(shouldShowLock);
    if (!shouldShowLock) {
      setFormData(prev => ({
        ...prev,
        lockDate: undefined,
        lockType: undefined,
        cancelLock: false
      }));
    }
  }, [formData.reasonLevel1]);

  const fetchReasonCodes = async () => {
    try {
      // Mock data - replace with actual API call
      const mockReasons: ReasonCode[] = [
        { id: 'financial_difficulty', name: 'Khó khăn tài chính', level: 1 },
        { id: 'service_issue', name: 'Vấn đề dịch vụ', level: 1 },
        { id: 'lock_after_level1_and_end_of_month', name: 'Mục 2: Khóa sau mục 1 và đến cuối tháng khóa hết', level: 1 },
        { id: 'temporary_financial', name: 'Khó khăn tài chính tạm thời', level: 2, parentId: 'financial_difficulty' },
        { id: 'permanent_financial', name: 'Khó khăn tài chính lâu dài', level: 2, parentId: 'financial_difficulty' },
        { id: 'internet_slow', name: 'Internet chậm', level: 2, parentId: 'service_issue' },
        { id: 'frequent_disconnection', name: 'Mất kết nối thường xuyên', level: 2, parentId: 'service_issue' }
      ];
      setReasonCodes(mockReasons);
    } catch (error) {
      console.error('Failed to fetch reason codes:', error);
    }
  };

  const validateForm = (): string | null => {
    if (!formData.reasonLevel1) return 'Vui lòng nhập đầy đủ thông tin';
    if (!formData.reasonLevel2) return 'Vui lòng chọn nguyên nhân cấp 2';
    if (showLevel3 && !formData.reasonLevel3) return 'Vui lòng chọn nguyên nhân cấp 3';
    if (!formData.notes.trim()) return 'Vui lòng nhập ghi chú';
    
    // Validate lock date if applicable
    if (showLockScheduling && formData.lockDate && !formData.cancelLock) {
      const today = new Date();
      const lockDate = new Date(formData.lockDate);
      const day = lockDate.getDate();
      
      if (day < 13) {
        return 'Thao tác thất bại. Chỉ cho phép cập nhật lịch khóa từ ngày 13 đến cuối tháng và không cho phép chọn ngày khóa nhỏ hơn hoặc bằng ngày hiện tại.';
      }
      
      if (lockDate <= today) {
        return 'Thao tác thất bại. Chỉ cho phép cập nhật lịch khóa từ ngày 13 đến cuối tháng và không cho phép chọn ngày khóa nhỏ hơn hoặc bằng ngày hiện tại.';
      }
      
      if (!formData.lockType) {
        return 'Vui lòng chọn trạng thái khóa';
      }
    }
    
    return null;
  };

  const handleSubmit = () => {
    const validationError = validateForm();
    if (validationError) {
      alert(validationError);
      return;
    }
    
    onSubmit(formData);
  };

  const level1Options = reasonCodes.filter(reason => reason.level === 1);

  return (
    <Card className="max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>Trả lý do không thanh toán</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Reason Level 1 */}
        <div className="space-y-2">
          <Label htmlFor="reasonLevel1">Nguyên nhân cấp 1 *</Label>
          <Select
            value={formData.reasonLevel1}
            onValueChange={(value) => setFormData(prev => ({ ...prev, reasonLevel1: value }))}
          >
            <SelectTrigger>
              <SelectValue placeholder="Chọn nguyên nhân cấp 1" />
            </SelectTrigger>
            <SelectContent>
              {level1Options.map((reason) => (
                <SelectItem key={reason.id} value={reason.id}>
                  {reason.name}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Reason Level 2 */}
        {formData.reasonLevel1 && (
          <div className="space-y-2">
            <Label htmlFor="reasonLevel2">Nguyên nhân cấp 2 *</Label>
            <Select
              value={formData.reasonLevel2}
              onValueChange={(value) => setFormData(prev => ({ ...prev, reasonLevel2: value }))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Chọn nguyên nhân cấp 2" />
              </SelectTrigger>
              <SelectContent>
                {level2Options.map((reason) => (
                  <SelectItem key={reason.id} value={reason.id}>
                    {reason.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Reason Level 3 */}
        {showLevel3 && (
          <div className="space-y-2">
            <Label htmlFor="reasonLevel3">Nguyên nhân cấp 3 *</Label>
            <Select
              value={formData.reasonLevel3 || ''}
              onValueChange={(value) => setFormData(prev => ({ ...prev, reasonLevel3: value }))}
            >
              <SelectTrigger>
                <SelectValue placeholder="Chọn nguyên nhân cấp 3" />
              </SelectTrigger>
              <SelectContent>
                {level3Options.map((reason) => (
                  <SelectItem key={reason.id} value={reason.id}>
                    {reason.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        )}

        {/* Notes */}
        <div className="space-y-2">
          <Label htmlFor="notes">Ghi chú *</Label>
          <Textarea
            id="notes"
            placeholder="Nhập thông tin ghi chú..."
            value={formData.notes}
            onChange={(e) => setFormData(prev => ({ ...prev, notes: e.target.value }))}
            className="min-h-[80px]"
          />
        </div>

        {/* Scheduled Date */}
        <div className="space-y-2">
          <Label>Ngày hẹn thanh toán</Label>
          <div className="flex space-x-4">
            <Popover>
              <PopoverTrigger asChild>
                <Button
                  variant="outline"
                  className={cn(
                    "justify-start text-left font-normal",
                    !formData.scheduledDate && "text-muted-foreground"
                  )}
                >
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {formData.scheduledDate ? format(formData.scheduledDate, "dd/MM/yyyy") : "Chọn ngày"}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0">
                <Calendar
                  mode="single"
                  selected={formData.scheduledDate}
                  onSelect={(date) => setFormData(prev => ({ ...prev, scheduledDate: date }))}
                  disabled={(date) => date < new Date()}
                  initialFocus
                />
              </PopoverContent>
            </Popover>
            
            {formData.scheduledDate && (
              <div className="flex items-center space-x-2">
                <Clock className="h-4 w-4" />
                <Select
                  value={formData.scheduledTime}
                  onValueChange={(value) => setFormData(prev => ({ ...prev, scheduledTime: value }))}
                >
                  <SelectTrigger className="w-32">
                    <SelectValue placeholder="Giờ" />
                  </SelectTrigger>
                  <SelectContent>
                    {Array.from({ length: 24 }, (_, i) => (
                      <SelectItem key={i} value={`${i.toString().padStart(2, '0')}:00`}>
                        {`${i.toString().padStart(2, '0')}:00`}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            )}
          </div>
        </div>

        {/* Lock Scheduling - Only for Debt Collection */}
        {isDebtCollection && showLockScheduling && (
          <div className="space-y-4 border-t pt-4">
            <Label>Ngày dự kiến khóa cước</Label>
            
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <input
                  type="radio"
                  id="cancelLock"
                  name="lockOption"
                  checked={formData.cancelLock}
                  onChange={() => setFormData(prev => ({ ...prev, cancelLock: true, lockDate: undefined, lockType: undefined }))}
                />
                <Label htmlFor="cancelLock">Hủy lịch khóa</Label>
              </div>
              
              <div className="flex items-center space-x-4">
                <input
                  type="radio"
                  id="setLockDate"
                  name="lockOption"
                  checked={!formData.cancelLock}
                  onChange={() => setFormData(prev => ({ ...prev, cancelLock: false }))}
                />
                <Label htmlFor="setLockDate">Chọn ngày khóa</Label>
              </div>
            </div>

            {!formData.cancelLock && (
              <div className="ml-6 space-y-4">
                <Popover>
                  <PopoverTrigger asChild>
                    <Button
                      variant="outline"
                      className={cn(
                        "justify-start text-left font-normal",
                        !formData.lockDate && "text-muted-foreground"
                      )}
                    >
                      <CalendarIcon className="mr-2 h-4 w-4" />
                      {formData.lockDate ? format(formData.lockDate, "dd/MM/yyyy") : "Chọn ngày khóa"}
                    </Button>
                  </PopoverTrigger>
                  <PopoverContent className="w-auto p-0">
                    <Calendar
                      mode="single"
                      selected={formData.lockDate}
                      onSelect={(date) => setFormData(prev => ({ ...prev, lockDate: date }))}
                      disabled={(date) => {
                        const day = date.getDate();
                        return date <= new Date() || day < 13;
                      }}
                      initialFocus
                    />
                  </PopoverContent>
                </Popover>

                {formData.lockDate && (
                  <div className="space-y-2">
                    <Label>Trạng thái khóa *</Label>
                    <Select
                      value={formData.lockType || ''}
                      onValueChange={(value: 'permanent' | 'temporary') => 
                        setFormData(prev => ({ ...prev, lockType: value }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Chọn trạng thái" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="permanent">Duy trì</SelectItem>
                        <SelectItem value="temporary">Tạm thời</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex justify-end space-x-4">
          <Button variant="outline" onClick={onCancel}>
            Hủy
          </Button>
          <Button onClick={handleSubmit}>
            Cập nhật
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default NonPaymentReasonForm;