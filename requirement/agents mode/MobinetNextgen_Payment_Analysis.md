# Module Thanh toán - Payment Analysis

**[⬅️ Quay lại Master Analysis](./MobinetNextgen_Master_Analysis.md)**

## Thông tin module | Module Information

- **Tên module:** Thanh toán (Payment)
- **Loại:** Upgrade
- **Mô tả:** Chức năng thực hiện thanh toán khoản thu và hóa đơn
- **Actors:** TIN/PNC, Thu cước
- **Trigger:** Nhấn thanh toán
- **Priority:** Critical - Core business function

## Sơ đồ tổng quan luồng thanh toán | Payment Flow Overview

```mermaid
flowchart TD
    Start([Khởi tạo thanh toán]) --> LoadData[Load dữ liệu hóa đơn và khoản thu]
    LoadData --> ValidateUser{Kiểm tra quyền user}
    
    ValidateUser -->|TIN/PNC| TINFlow[Quy trình TIN/PNC]
    ValidateUser -->|Thu cước| CUSFlow[Quy trình Thu cước]
    
    TINFlow --> PTCCheck{Có khoản thu PTC?}
    PTCCheck -->|Có| ForceSelectPTC[Bắt buộc chọn PTC]
    PTCCheck -->|Không| SelectItems[Chọn hóa đơn/khoản thu]
    
    CUSFlow --> AutoSelectNormal{HĐ Bình thường?}
    AutoSelectNormal -->|Có| AutoCheck[Tự động check tất cả HĐ]
    AutoSelectNormal -->|Không| SelectItems
    
    ForceSelectPTC --> SelectItems
    AutoCheck --> SelectItems
    
    SelectItems --> ValidateSelection{Kiểm tra rule thanh toán}
    
    ValidateSelection -->|Lỗi| ShowError[Hiển thị lỗi]
    ValidateSelection -->|OK| ChoosePaymentMethod[Chọn phương thức thanh toán]
    
    ShowError --> SelectItems
    
    ChoosePaymentMethod -->|Tiền mặt tạm| CashPayment[Thanh toán tạm]
    ChoosePaymentMethod -->|FPT Pay| FPTPayment[Thanh toán FPT Pay]
    ChoosePaymentMethod -->|QR Code| QRPayment[Thanh toán QR]
    
    CashPayment --> ProcessPayment[Xử lý thanh toán]
    FPTPayment --> ProcessPayment
    QRPayment --> ProcessPayment
    
    ProcessPayment --> Success{Thành công?}
    Success -->|Có| SendNotification[Gửi thông báo]
    Success -->|Không| PaymentError[Lỗi thanh toán]
    
    SendNotification --> UpdateSystem[Cập nhật hệ thống]
    UpdateSystem --> End([Hoàn thành])
    
    PaymentError --> ChoosePaymentMethod
    
    style Start fill:#e8f5e8
    style End fill:#e8f5e8
    style ProcessPayment fill:#bbdefb
    style Success fill:#c8e6c9
    style ShowError fill:#ffcdd2
    style PaymentError fill:#ffcdd2
```

## Chi tiết các phương thức thanh toán | Payment Methods Details

### 1. Thanh toán tạm (Temporary Cash Payment)

```mermaid
sequenceDiagram
    participant User as Nhân viên
    participant App as Mobile App
    participant Backend as Hệ thống Backend
    participant Limit as Hạn mức Service
    participant Notification as Thông báo Service
    
    User->>App: Chọn "Tiền mặt tạm"
    App->>Limit: Kiểm tra hạn mức
    Limit-->>App: Thông tin hạn mức
    
    alt Đủ hạn mức
        App->>Backend: Thực hiện thanh toán tạm
        Backend->>Backend: Cập nhật số dư tạm
        Backend-->>App: Thanh toán thành công
        App->>Notification: Gửi thông báo xác nhận
        App->>User: Hiển thị thành công
    else Vượt hạn mức
        App->>User: Thông báo "Vượt quá hạn mức gạch nợ bằng tiền mặt"
    end
```

### 2. Thanh toán FPT Pay

```mermaid
sequenceDiagram
    participant User as Nhân viên
    participant App as Mobile App
    participant FPTPay as FPT Pay Gateway
    participant Backend as Hệ thống Backend
    
    User->>App: Chọn "Ví FPT Pay"
    App->>App: Kiểm tra liên kết ví
    
    alt Chưa liên kết
        App->>User: "Vui lòng thực hiện liên kết phương thức thanh toán"
    else Đã liên kết
        App->>FPTPay: Khởi tạo thanh toán
        FPTPay->>User: Yêu cầu xác thực (OTP/Password)
        User->>FPTPay: Nhập thông tin xác thực
        
        alt Xác thực thành công
            FPTPay->>Backend: Xác nhận thanh toán
            Backend-->>App: Thanh toán thành công
            App->>User: Hiển thị kết quả thành công
        else Xác thức thất bại
            FPTPay-->>App: Thanh toán thất bại
            App->>User: Hiển thị lỗi
        end
    end
```

### 3. Thanh toán QR Code VN Pay

```mermaid
sequenceDiagram
    participant User as Nhân viên
    participant Customer as Khách hàng
    participant App as Mobile App
    participant VNPay as VN Pay Gateway
    participant Backend as Hệ thống Backend
    
    User->>App: Chọn "QR Pay - VN Pay"
    App->>VNPay: Tạo mã QR thanh toán
    VNPay-->>App: Mã QR
    App->>User: Hiển thị mã QR
    
    User->>Customer: Cung cấp mã QR
    Customer->>VNPay: Quét mã QR và thanh toán
    VNPay->>Backend: Thông báo thanh toán thành công
    
    loop Kiểm tra trạng thái thanh toán
        User->>App: Nhấn "Kiểm tra thanh toán"
        App->>Backend: Kiểm tra trạng thái
        alt Chưa thanh toán
            Backend-->>App: "Chưa thanh toán"
        else Đã thanh toán
            Backend-->>App: "Thanh toán thành công"
            App->>User: Hiển thị kết quả
        end
    end
```

## Business Rules chi tiết | Detailed Business Rules

### BR.1 - Hiển thị thông tin thanh toán

#### Thông tin khách hàng
- **Hợp đồng:** Số hợp đồng khách hàng
- **Khách hàng:** Tên đầy đủ khách hàng
- **Số điện thoại:** Logic chọn SĐT phức tạp:

```mermaid
flowchart TD
    CheckSetting{Kiểm tra cài đặt gửi thông báo}
    CheckSetting -->|HiFPT only| HiFPTFlow[Chọn SĐT theo HiFPT]
    CheckSetting -->|HiFPT + SMS/ZNS| BothFlow[Chọn SĐT cho cả 2 kênh]
    
    HiFPTFlow --> CheckMainHiFPT{SĐT chính có HiFPT?}
    CheckMainHiFPT -->|Có| ShowMain[Hiển thị SĐT chính]
    CheckMainHiFPT -->|Không| CheckOtherHiFPT{SĐT khác có HiFPT?}
    CheckOtherHiFPT -->|Có| ShowOther[Hiển thị SĐT có HiFPT]
    CheckOtherHiFPT -->|Không| ShowEmpty[Để trống]
    
    BothFlow --> ShowMainDefault[Mặc định hiển thị SĐT chính]
    
    style CheckSetting fill:#e3f2fd
    style ShowMain fill:#c8e6c9
    style ShowOther fill:#c8e6c9
    style ShowEmpty fill:#ffecb3
```

#### Danh sách hóa đơn
- **Số hóa đơn:** Mã định danh hóa đơn
- **Thời gian:** Từ ngày - Đến ngày (theo tool liệt kê cước)
- **Số tiền:** Giá trị hóa đơn bao gồm VAT
- **Nội dung:** Mô tả tổng hợp hóa đơn
- **Tích chọn:** Logic phức tạp theo role và trạng thái

#### Danh sách khoản thu
- **Nội dung:** Mô tả khoản thu
- **Số khoản thu:** Mã định danh
- **Số tiền:** Giá trị cần thu
- **Nguồn:** Loại trừ recare trả trước (PaidType = 2), titok, shopee
- **Tích chọn:** Theo quy tắc role cụ thể

### BR.2 - Rules thanh toán

#### Rule chung
1. **Thanh toán hóa đơn xa nhất trước**
   ```
   IF (Ngày phát hành HĐ được chọn > Ngày PH của HĐ chưa chọn)
   THEN Hiển thị: "Vui lòng thanh toán hóa đơn xa nhất"
   ```

2. **Tồn tạm chưa nộp tiền về công ty**
   ```
   IF (10h ngày hôm sau AND Tài khoản còn tồn tạm ngày hôm trước)
   THEN Không cho thanh toán: "Đang tồn tạm không thể thanh toán"
   ```

3. **Hạn mức thanh toán**
   ```
   IF (Hạn mức còn lại < Tổng tiền thanh toán)
   THEN Hiển thị: "Vượt quá hạn mức gạch nợ bằng tiền mặt"
   ```

4. **Giới hạn số lượng**
   ```
   IF (Số HĐ + Khoản thu được chọn > 6)
   THEN Hiển thị: "Chỉ được chọn tối đa 6 hóa đơn/khoản thu thanh toán"
   ```

#### Rule theo role TIN/PNC
```mermaid
flowchart TD
    CheckRole{Role = TIN/PNC?}
    CheckRole -->|Có| CheckPTC{Có khoản thu PTC?}
    CheckRole -->|Không| OtherRole[Áp dụng rule khác]
    
    CheckPTC -->|Có| ForcePTC[Bắt buộc thanh toán PTC]
    CheckPTC -->|Không| OptionalOther[Khoản thu khác không bắt buộc]
    
    ForcePTC --> CheckHMBS{Nhân sự có HMBS?}
    CheckHMBS -->|Có| ApplyHMBS[Áp dụng hạn mức bổ sung]
    CheckHMBS -->|Không| NormalLimit[Áp dụng hạn mức thường]
    
    style CheckRole fill:#e3f2fd
    style ForcePTC fill:#ffcc02
    style ApplyHMBS fill:#c8e6c9
```

#### Rule theo role Thu cước
```mermaid
flowchart TD
    CheckContract{Loại hợp đồng?}
    CheckContract -->|Bình thường| CheckSR{Có SR KPDV "đang xử lý"?}
    CheckContract -->|Khác Bình thường| CheckSRSpecial{Có SR KPDV "đang xử lý"?}
    
    CheckSR -->|Có| ForcePayBill[Bắt buộc thanh toán HĐ]
    CheckSR -->|Không| OptionalBill[Không bắt buộc thanh toán HĐ]
    
    CheckSRSpecial -->|Không| ForcePayBill
    CheckSRSpecial -->|Có| OptionalBill
    
    ForcePayBill --> CheckSMSLimit[Kiểm tra giới hạn SMS/ZNS]
    OptionalBill --> CheckSMSLimit
    
    CheckSMSLimit --> SMSRule{Số lần gửi trong tháng}
    SMSRule -->|<= 10 lần| AllowSMS[Cho phép gửi SMS]
    SMSRule -->|> 10 lần| BlockSMS[Chặn gửi: "SĐT đã gửi quá 10 lần trong tháng"]
    
    style CheckContract fill:#e3f2fd
    style ForcePayBill fill:#ffcc02
    style BlockSMS fill:#ffcdd2
```

## Templates thông báo | Notification Templates

### Template SMS Kỹ thuật
```
FPT Telecom thong bao: So tien Quy khach thanh toan cho HD [SoHD] la [SoTien] VND. 
Xin cam on. (ISC01.TRANGPT30)
```

### Template SMS Thu cước
```
Cam on ban da thanh toan thanh cong so [SoTien]d, so chung tu: [SoChungTu] 
tu ngay [TuNgay] – [DenNgay] cua hop dong [SoHD]. LH 19006600
```

### Template ZNS Zalo
```mermaid
graph LR
    A[Template ZNS] --> B[Thông tin xác nhận thanh toán]
    B --> C[Địa chỉ lập hóa đơn]
    B --> D[Số chứng từ và kỳ cước]
    B --> E[Tổng tiền và số tiền đã thanh toán]
    B --> F[Thanh toán bằng phương thức]
    B --> G[Ngày thanh toán]
    B --> H[Tích lũy FGold]
    
    style A fill:#e3f2fd
    style B fill:#f3e5f5
```

### Template HiFPT
- **Giao diện rich media:** Banner, thông tin chi tiết, link truy cập
- **Nút tương tác:** "Đăng ký trả trước" với deep link
- **Tracking:** FGold points và promotion information

## Wireframes và giao diện | UI/UX Specifications

### Màn hình thanh toán chính
- **Header:** Thông tin khách hàng, số điện thoại
- **Body:** 
  - Danh sách hóa đơn với checkbox
  - Danh sách khoản thu với checkbox
  - Tổng tiền thanh toán
- **Footer:** Nút "Thanh toán" với validation

### Màn hình chọn phương thức thanh toán
- **Tiền mặt tạm:** Hiển thị hạn mức còn lại
- **Ví FPT Pay:** Trạng thái liên kết + thông tin ví
- **Mã QR:** Generator QR code + hướng dẫn

### Màn hình thiết lập thông báo
- **Toggle HiFPT:** Luôn bật cho Thu cước
- **Toggle SMS/ZNS:** Có thể bật/tắt
- **Danh sách SĐT:** Với icon HiFPT indicator
- **Hạn mức SMS:** Hiển thị quota còn lại

## Testing scenarios | Kịch bản kiểm thử

### Test Case 1: Thanh toán thành công cơ bản
```
Precondition: User đăng nhập thành công, có hóa đơn cần thanh toán
Steps:
1. Vào màn hình thanh toán
2. Chọn 1 hóa đơn
3. Chọn "Tiền mặt tạm"
4. Xác nhận thanh toán
Expected: Thanh toán thành công, gửi thông báo, cập nhật hệ thống
```

### Test Case 2: Vượt hạn mức
```
Precondition: Hạn mức < Tổng tiền cần thanh toán
Steps:
1. Chọn hóa đơn có tổng tiền > hạn mức
2. Nhấn "Thanh toán"
Expected: Hiển thị "Vượt quá hạn mức gạch nợ bằng tiền mặt"
```

### Test Case 3: Rule thanh toán xa nhất
```
Precondition: Có nhiều hóa đơn với ngày phát hành khác nhau
Steps:
1. Chọn hóa đơn gần đây, bỏ qua hóa đơn xa
2. Nhấn "Thanh toán"
Expected: "Vui lòng thanh toán hóa đơn xa nhất"
```

## Integration points | Điểm tích hợp

### Hệ thống nội bộ
- **Tool Liệt kê cước:** GET bill details, service breakdown
- **Tool Đối soát khoản thu:** GET payment fees, transaction history  
- **Hạn mức Service:** GET/UPDATE credit limits
- **Tool Chăm sóc KH:** POST customer care information

### External APIs
- **FPT Pay Gateway:** Payment processing, wallet linking
- **VN Pay QR:** QR code generation, payment verification
- **HiFPT API:** Rich notification delivery
- **SMS/ZNS Gateway:** Text message delivery

---

**[⬅️ Quay lại Master Analysis](./MobinetNextgen_Master_Analysis.md)**

**Liên quan:** 
- [Module Trả lý do không thanh toán](./MobinetNextgen_NonPaymentReason_Analysis.md)
- [Module Xem hạn mức thanh toán](./MobinetNextgen_PaymentLimit_Analysis.md)
- [Module Liên kết ví/Ngân hàng](./MobinetNextgen_WalletBanking_Analysis.md)