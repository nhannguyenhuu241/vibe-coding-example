# Non-Payment Reason Analysis Module

## Tổng quan | Overview

Module **Trả lý do không thanh toán** được phát triển theo đặc tả từ tài liệu `MobinetNextgen_NonPaymentReason_Analysis.md`. Module này cho phép nhân viên Thu cước cập nhật lý do khách hàng không thanh toán, thiết lập ngày hẹn và quản lý lịch khóa cước.

## Cấu trúc dự án | Project Structure

```
src/
├── components/
│   └── NonPaymentReasonForm.tsx           # Main form component
├── pages/
│   ├── api/
│   │   ├── non-payment-reasons/
│   │   │   ├── level1.ts                  # API lấy nguyên nhân cấp 1
│   │   │   ├── level2.ts                  # API cascade nguyên nhân cấp 2
│   │   │   ├── level3.ts                  # API cascade nguyên nhân cấp 3
│   │   │   └── submit.ts                  # API submit form + tích hợp hệ thống
│   │   └── non-payment-history.ts         # API lịch sử cập nhật
│   └── non-payment-reason.tsx             # Demo page
├── store/
│   └── nonPaymentReasonStore.ts           # Zustand state management
├── types/
│   └── nonPaymentReason.ts                # TypeScript interfaces
├── constants/
│   └── nonPaymentReason.ts                # Constants và validation messages
├── utils/
│   └── nonPaymentValidation.ts            # Business rules validation
├── hooks/
│   └── useNonPaymentReasonForm.ts         # Custom hook cho form logic
└── styles/
    └── globals.css                        # Custom CSS animations
```

## Tính năng chính | Key Features

### ✅ Implemented Features

1. **Cascade Loading Nguyên nhân 3 cấp**
   - Level 1 → Level 2 → Level 3 (conditional)
   - Auto-refresh khi thay đổi cấp cha
   - Loading states với shimmer effect

2. **Form Validation**
   - Client-side validation với business rules
   - Server-side validation trong API
   - Real-time error display
   - Focus management cho accessibility

3. **Role-based Permissions**
   - Thu cước: Full access + lock date management
   - Nhân viên khác: Chỉ form cơ bản

4. **Lock Date Management**
   - 3 frames theo thiết kế UX
   - Date range validation (ngày 13 - cuối tháng)
   - Lock status selection (Duy trì/Tạm thời)

5. **History Tracking**
   - Hiển thị lịch sử trong tháng
   - Sort theo thời gian mới nhất
   - Collapsible UI component

6. **System Integration**
   - Tool QL Công nợ DVKH/Quản Lý Khách Hàng
   - Tool Chăm sóc khách hàng (với field mapping)
   - Parallel API calls cho performance

7. **UI/UX Enhancements**
   - Mobile-first responsive design
   - Smooth animations (fade-in, slide-in)
   - Toast notifications
   - Loading states
   - Error states với visual feedback

## API Endpoints

### GET `/api/non-payment-reasons/level1`
Lấy danh sách nguyên nhân cấp 1
```typescript
Response: NonPaymentReason[]
```

### GET `/api/non-payment-reasons/level2?level1={id}`
Lấy danh sách nguyên nhân cấp 2 theo cấp 1
```typescript
Query: level1: string
Response: NonPaymentReason[]
```

### GET `/api/non-payment-reasons/level3?level1={id}&level2={id}`
Lấy danh sách nguyên nhân cấp 3 (conditional)
```typescript
Query: level1: string, level2: string
Response: NonPaymentReason[]
```

### POST `/api/non-payment-reasons/submit`
Submit form và tích hợp hệ thống
```typescript
Body: NonPaymentReasonFormData & { staffAccount: string }
Response: { success: boolean, message: string, errors?: ValidationError[] }
```

### GET `/api/non-payment-history?contractId={id}`
Lấy lịch sử cập nhật trong tháng
```typescript
Query: contractId: string
Response: NonPaymentHistory[]
```

## Business Rules Implementation

### BR.2.1 - Validation Rules
- ✅ Required field validation
- ✅ Date range validation (không chọn ngày quá khứ)
- ✅ Lock date validation (13-cuối tháng, > ngày hiện tại)
- ✅ Note max length (500 characters)
- ✅ Conditional level 3 validation

### BR.2.2 - System Integration
- ✅ Parallel updates to multiple systems
- ✅ Field mapping cho Care System
- ✅ Transaction rollback handling
- ✅ Error handling và logging

## Cách sử dụng | How to Use

### 1. Chạy development server
```bash
npm run dev
```

### 2. Truy cập demo page
```
http://localhost:3000/non-payment-reason
```

### 3. Chọn user role để test
- **Thu cước**: Có tất cả tính năng + quản lý khóa cước
- **Nhân viên khác**: Chỉ form cơ bản

### 4. Test scenarios
- Happy path: Fill toàn bộ form và submit
- Validation: Bỏ trống required fields
- Cascade: Chọn nguyên nhân có/không có level 3
- Lock date: Test date range validation
- History: View lịch sử cập nhật

## State Management

Sử dụng **Zustand** cho state management với các features:
- Devtools integration
- Persistent state
- Async actions
- Error handling
- Loading states

### Store Structure
```typescript
interface NonPaymentReasonState {
  reasons: { level1, level2, level3 }
  formData: NonPaymentReasonFormData
  history: NonPaymentHistory[]
  isLoading: boolean
  errors: ValidationError[]
  currentUser: UserRole
}
```

## Styling & Animations

### CSS Classes được implement
- `.animate-fade-in`: Fade in animation
- `.animate-shimmer`: Loading skeleton
- `.animate-slide-in`: Slide in from bottom
- `.loading-skeleton`: Shimmer loading effect
- `.form-field-error`: Error state styling
- `.dropdown-loading`: Loading dropdown indicator

### Responsive Design
- Mobile-first approach
- Tailwind CSS utilities
- Custom breakpoints
- Touch-friendly interactions

## Testing Scenarios

### Test Case 1: Happy Path (Thu cước)
1. Select user: Thu cước
2. Choose reason level 1: "Khách hàng không có mặt"
3. Choose reason level 2: "Đi công tác"  
4. Enter note: "Khách hàng đi công tác 1 tuần"
5. Set appointment date: Tomorrow 9:00 AM
6. Set lock date: Day 15 of current month
7. Select lock status: "Duy trì"
8. Submit form
9. **Expected**: Success message, data saved to history

### Test Case 2: Validation Errors
1. Leave all required fields empty
2. Submit form
3. **Expected**: All validation error messages displayed

### Test Case 3: Lock Date Validation
1. Select user: Thu cước
2. Choose lock date < day 13 or <= current date
3. Submit form
4. **Expected**: Lock date error message

### Test Case 4: Cascade Loading
1. Choose level 1 reason that has level 2
2. Choose level 2 reason that has level 3
3. **Expected**: Level 3 dropdown appears with animation

## Performance Optimizations

1. **API Caching**: Level 1 reasons cached for 1 hour
2. **Debounced Validation**: Form validation debounced 300ms
3. **Lazy Loading**: History loaded on demand
4. **Parallel Requests**: Multiple system updates in parallel
5. **Bundle Optimization**: Code splitting và tree shaking

## Security Considerations

1. **Input Validation**: Both client và server-side
2. **SQL Injection Protection**: Parameterized queries
3. **XSS Prevention**: Input sanitization
4. **Role-based Access**: Permission checking
5. **Rate Limiting**: API throttling
6. **Audit Logging**: All actions logged

## Future Enhancements

### Phase 2 Features
- [ ] Offline support với Service Worker
- [ ] Push notifications cho due dates
- [ ] Advanced history filtering
- [ ] Export lịch sử ra Excel/PDF
- [ ] Multi-language support
- [ ] Voice input cho ghi chú
- [ ] AI-powered reason suggestion

### Technical Improvements
- [ ] Unit tests với Jest + React Testing Library
- [ ] E2E tests với Playwright
- [ ] Performance monitoring
- [ ] Error tracking với Sentry
- [ ] Analytics integration
- [ ] CI/CD pipeline

## Troubleshooting

### Common Issues

1. **API không load được reasons**
   - Check network tab trong DevTools
   - Verify API endpoints đang chạy
   - Check CORS settings

2. **Form validation không hoạt động**
   - Check browser console for errors
   - Verify validation rules trong utils/nonPaymentValidation.ts
   - Check form data structure

3. **History không hiển thị**
   - Verify contractId được pass correctly
   - Check API response trong Network tab
   - Verify date filtering logic

4. **Lock date validation issues**
   - Check system date
   - Verify date format và timezone
   - Check business rules implementation

### Debug Mode
Enable debug logging:
```javascript
localStorage.setItem('non-payment-debug', 'true');
```

## Contributing

1. Follow TypeScript strict mode
2. Use Prettier for code formatting
3. Write JSDoc comments for public APIs
4. Add unit tests for new features
5. Update this README for new functionality

## Dependencies

### Production
- `next`: 14.0.3 - React framework
- `react`: 18.2.0 - UI library  
- `zustand`: 4.4.7 - State management
- `date-fns`: 2.30.0 - Date utilities
- `react-hook-form`: 7.48.2 - Form handling
- `react-hot-toast`: 2.4.1 - Toast notifications
- `@headlessui/react`: 1.7.17 - UI components
- `@heroicons/react`: 2.0.18 - Icons
- `tailwindcss`: 3.3.6 - CSS framework
- `zod`: 3.22.4 - Schema validation

### Development
- `typescript`: 5.3.2 - Type checking
- `@types/*`: Type definitions
- `eslint`: 8.54.0 - Linting
- `prettier`: 3.1.0 - Code formatting

---

**Tác giả**: Development Team  
**Phiên bản**: 1.0.0  
**Cập nhật cuối**: $(date)  
**Liên hệ**: [development@company.com]