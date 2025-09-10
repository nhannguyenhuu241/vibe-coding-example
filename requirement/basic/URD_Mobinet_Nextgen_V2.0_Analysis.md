# Mobinet Nextgen VER 2.0 - User Requirements Document (URD) Analysis

## Document Information

| Field | Value |
|-------|--------|
| Document Code | 1.0-BM/PM/HDCV/FTEL |
| Version | 1.1 |
| Created | 18/7/2025 |
| Author | ThaoNTH9 |
| Reviewer | GiauTQ |
| Status | Initial Document |

## Revision History

| Date | Version | Author | Reviewer | Change Description |
|------|---------|--------|----------|-------------------|
| 18/7/2025 | 1.0 | ThaoNTH9 | GiauTQ | Khởi tạo tài liệu |

**Change Legend:**
- [A]: Add – Thêm mới
- [U]: Update – Cập nhật, thay đổi  
- [D]: Delete - Xóa

---

# 1. GIỚI THIỆU

## 1.1 Mục đích tài liệu

Tài liệu mô tả và phác thảo yêu cầu của người dùng cuối. Giúp đơn vị yêu cầu và các thành viên dự án xác định đúng và đủ yêu cầu.

**Tài liệu này là cơ sở và đầu vào cho các quá trình:**
- Thu thập, phân tích yêu cầu, đưa ra đặc tả yêu cầu phần mềm
- Phân tích thiết kế, lập trình
- Kiểm thử phần mềm
- Nghiệm thu

## 1.2 Thông tin chung

### Dự án Overview

| STT | Hạng mục | Mô tả |
|-----|----------|-------|
| 1 | Giới thiệu tổng quan | Xây dựng SDK thanh toán hóa đơn, khoản thu phục vụ cho Sale, TIN/PNC, Thu cước |
| 2 | Hiện trạng | Cải tiến chức năng cũ và bổ sung chức năng mới |
| 3 | Mục tiêu/Hiệu quả kỳ vọng | Áp dụng cho tất cả nhân viên Sale, thu cước và kỹ thuật viên. Thực hiện thanh toán hóa đơn và khoản thu của khách hàng |
| 4 | Domain nghiệp vụ | Thanh toán hóa đơn, khoản thu |

## 1.3 Thuật ngữ, từ ngữ viết tắt

| Thuật ngữ | Mô tả |
|-----------|-------|
| PO | Product owner |
| ĐVYC | Đơn vị yêu cầu |
| ISC | Trung tâm Hệ thống thông tin |
| PM | Project manager |
| BA | Business analyst |
| TL | Team leader |
| PIC | Person in charge |

---

# 2. TỔNG QUAN

## 2.1 Danh sách các chức năng

| # | Chức năng | Loại | Mô tả |
|---|-----------|------|--------|
| 1 | Thanh toán | Upgrade | Hiển thị danh sách, hóa đơn khoản thu thanh toán |
| 2 | Trả lý do không thanh toán | Upgrade | Cập nhật trả lý do không thanh toán<br/>Cập nhật thông tin ngày hẹn thanh toán, ngày dự kiến khóa cước |
| 3 | Xem hạn mức thanh toán | Upgrade | Xem hạn mức thanh toán |
| 4 | Liên kết ví/Ngân hàng | Upgrade | Liên kết ví hoặc tài khoản ngân hàng |
| 5 | Thiết lập gửi tin nhắn | Upgrade | Thiết lập gửi tin nhắn qua HiFPT hoặc SMS/ZNS |
| 6 | Thanh toán hợp đồng đại diện | Upgrade | Thanh toán hợp đồng đại diện |

**Design Reference:** [Figma Wireframes](https://www.figma.com/design/Ex8yecMU7ZfmHpYurQQRwW/MBX-T%C3%ADch-h%E1%BB%A3p?node-id=81-2734&t=58y2YFKmjccJFd57-1)

---

# 3. ĐẶC TẢ CÁC CHỨC NĂNG

## 3.1 Thanh toán

### 3.1.1 Use Case Overview

| Field | Value |
|-------|--------|
| **Description** | Chức năng thực hiện thanh toán khoản thu và hóa đơn |
| **Actor** | TIN/PNC, Thu cước |
| **Trigger** | Nhấn thanh toán |
| **Pre-condition** | - Người dùng mở app thành công<br/>- Nhân viên có hóa đơn, khoản thu cần thanh toán |
| **Post-condition** | Thanh toán thành công |

### 3.1.2 Workflow
- Luồng thanh toán trên MBN và MBP

### 3.1.3 Screen Components

**Màn hình Thanh toán bao gồm:**

#### Thông tin khách hàng:
- **Hợp đồng:** Hiển thị số hợp đồng
- **Khách hàng:** Hiển thị tên khách hàng
- **Số điện thoại:** Load 1 SĐT được chọn ra màn hình Thanh toán

**Quy tắc hiển thị SĐT:**

**Trường hợp gửi qua HiFPT, không gửi qua Zalo/SMS:**
1. Nếu SĐT chính chủ cài app HiFPT ⇒ Hiển thị SĐT chính chủ
2. Nếu SĐT chính chủ không cài app HiFPT ⇒ Lấy 1 SĐT nhắn tin bất kỳ có cài app HiFPT
3. Nếu danh sách SĐT không có SĐT nào cài app HiFPT ⇒ Để trống

**Trường hợp gửi qua HiFPT và Zalo/SMS:**
- Hiển thị SĐT đã chọn tại màn hình Thanh toán
- Mặc định hiển thị SĐT chính chủ

#### Danh sách Hóa đơn:
- **Số hóa đơn:** Hiển thị số hóa đơn
- **Thời gian:** Hiển thị Từ ngày – Đến ngày (Trên tool liệt kê cước)
- **Số tiền:** Hiển thị số tiền hóa đơn  
- **Nội dung:** Hiển thị nội dung tổng hóa đơn
- **Tích chọn:** 1 hoặc nhiều hóa đơn. Mặc định ban đầu uncheck

**Quy tắc tích chọn hóa đơn:**
- Nếu nhân viên thu cước, HĐ khác "Bình thường" (trừ TH có SR KPDV "đang xử lý") ⇒ Hệ thống tự động check chọn tất cả hóa đơn và không cho uncheck

#### Danh sách Khoản thu:
- **Nội dung:** Hiển thị nội dung khoản thu
- **Số khoản thu:** Hiển thị số khoản thu
- **Số tiền:** Hiển thị số tiền khoản thu
- **Nguồn:** Hiển thị tất cả khoản thu (trừ nguồn recare trả trước chưa thêm Phí thu tại nhà (PaidType = 2), nguồn titok, nguồn shopee)
- **Tích chọn:** 1 hoặc nhiều khoản thu. Mặc định ban đầu uncheck

**Quy tắc tích chọn khoản thu:**

**Đối với Kỹ thuật:**
- Nếu khoản thu được đẩy từ MBN ⇒ Hệ thống tự động check và không cho uncheck

**Đối với Thu cước:**
- Đi từ chức năng "Tham gia trả trước": Mặc định check vào các khoản thu Recare trả trước, cho phép bỏ check
- Đi từ chức năng "Thanh toán": Mặc định uncheck

### 3.1.4 Business Rules

#### Rule chung:
1. **Thanh toán hóa đơn xa nhất trước**
   - Nếu tích chọn hóa đơn có ngày phát hành lớn hơn ngày PH của các hóa đơn còn lại chưa tích chọn
   - Nhấn Tiếp tục tại màn hình PTTT ⇒ Hiển thị thông báo "Vui lòng thanh toán hóa đơn xa nhất"

2. **Tồn tạm chưa nộp tiền về công ty**
   - 10h ngày hôm sau (trừ T7,CN, lễ), tài khoản còn tồn tạm của ngày hôm trước trở về trước không cho thanh toán
   - Hiển thị thông báo "Đang tồn tạm không thể thanh toán"

3. **Hạn mức thanh toán**
   - Hạn mức còn lại >= Tổng tiền thanh toán
   - Nếu quá hạn mức hiển thị thông báo "Vượt quá hạn mức gạch nợ bằng tiền mặt"

4. **Hợp đồng chưa ký HĐĐT/PLHĐ/BBĐT**
   - Hiển thị thông báo "Hợp đồng SFAXXXX đang tồn tại HĐĐT/PLHĐ/BBĐT cần ký kết..."

5. **Giới hạn số lượng thanh toán**
   - Chỉ được chọn tối đa 6 hóa đơn và khoản thu cần thanh toán
   - Nếu chọn quá 6 khoản ⇒ Hiển thị thông báo "Chỉ được chọn tối đa 6 hóa đơn/khoản thu thanh toán"

#### Rule theo nhân sự:

**Nếu tài khoản nhân sự là TIN/PNC:**
- Bắt buộc phải thanh toán khoản thu từ PTC. Các khoản thu khác không bắt buộc
- Trường hợp nhân sự thuộc rule cấp hạn mức bổ sung: Hệ thống thực hiện thanh toán theo rule hạn mức bổ sung được cấp

**Nếu tài khoản nhân sự là Thu cước:**
- Đối với hợp đồng khác "Bình thường", trừ TH có vết SR KPDV "đang xử lý" ⇒ Nếu có hóa đơn bắt buộc thanh toán hóa đơn
- Đối với hợp đồng "Bình thường" hoặc có SR KPDV "đang xử lý" ⇒ Không bắt buộc thanh toán hóa đơn

#### Rule gửi thông báo:
- 1 SĐT chỉ gửi nhiều nhất 10 lần/tháng (đếm số lần gửi ZNS/SMS gửi thành công)
- Nếu 1 SĐT gửi >10 lần/tháng ⇒ Hiển thị thông báo "Số điện thoại đã gửi quá 10 lần trong tháng..."
- Thu cước đã hết số lượng gửi SMS/ZNS trong tháng ⇒ Hiển thị thông báo "Tài khoản đã hết số lần được gửi thông báo"

### 3.1.5 Payment Methods

#### 1. Thanh toán tạm
- Thanh toán thành công hiển thị thông báo xác nhận
- Nhấn nút đóng quay về màn hình Thanh toán và reload lại thông tin
- Trừ hạn mức thanh toán
- Các giao dịch thành công sẽ được đẩy vào hợp đồng đại diện để được gạch nợ bổ sung

#### 2. Thanh toán online từ tài khoản nhân viên

**Ví FPT Pay (Ví nhân viên):**
- Nhân sự dùng Ví FPT Pay đã liên kết để thanh toán đơn hàng thay KH
- Chọn PTTT Ví FPT Play gọi giao diện Foxpay thanh toán nhập mật khẩu (dưới 5tr) hoặc OTP (trên 5tr)
- Thanh toán thành công hiển thị thông báo và reload lại thông tin
- Nếu chưa liên kết ví ⇒ Hiển thị thông báo "Vui lòng thực hiện liên kết phương thức thanh toán"

#### 3. Thanh toán online từ khách hàng

**QR Pay – VN Pay:**
- Mã QR thanh toán sẽ gen trên app SDK thanh toán
- Nhân sự cung cấp mã trực tiếp mã QR hoặc chụp ảnh mã QR để KH thanh toán trên tất cả các ứng dụng thanh toán
- Có nút tải về để tải mã QRcode về máy
- Nút kiểm tra thanh toán để xác nhận trạng thái thanh toán

### 3.1.6 Payment Confirmation Messages

#### Gửi qua kênh HiFPT:
```
"Thanh toán thành công. Vui lòng kiểm tra xác nhận thanh toán qua ứng dụng HiFPT theo số điện thoại đã cài đặt: 0987843256, 0987563245

Nhấn nút copy gửi KH xác nhận thanh toán:
https://fpt.vn/pay/SGD565970*"
```

#### Gửi qua kênh ZNS/SMS:
```
"Thanh toán thành công. Vui lòng kiểm tra xác nhận thanh toán qua Zalo hoặc SMS theo số điện thoại: 0987843256

Nhấn nút copy gửi KH xác nhận thanh toán:
https://fpt.vn/pay/SGD565970*"
```

---

## 3.2 Trả lý do không thanh toán

### 3.2.1 Use Case Overview

| Field | Value |
|-------|--------|
| **Description** | Chức năng thực hiện cập nhật lý do không thanh toán |
| **Actor** | Thu cước |
| **Trigger** | Nhấn Cập nhật trả lý do không thanh toán |
| **Pre-condition** | Người dùng mở app thành công |
| **Post-condition** | Cập nhật trả lý do không thanh toán thành công |

### 3.2.2 Screen Components

**Nhấn "..." tại Tile màn hình Thanh toán hiển thị màn hình Trả lý do không thanh toán:**

#### Nguyên nhân cấp 1:
- Mặc định ban đầu chưa chọn nguyên nhân nào
- Load danh sách nguyên nhân cấp 1
- Chỉ chọn 1 giá trị
- Bắt buộc chọn, nếu chưa chọn nhấn nút Cập nhật hiển thị thông báo "Vui lòng nhập đầy đủ thông tin"

#### Nguyên nhân cấp 2:
- Mặc định ban đầu chưa chọn nguyên nhân nào
- Load danh sách nguyên nhân cấp 2 theo nguyên nhân cấp 1 đã chọn
- Chỉ chọn 1 giá trị
- Bắt buộc chọn

#### Nguyên nhân cấp 3:
- Mặc định ban đầu ẩn đi combo nguyên nhân cấp 3
- Load danh sách nguyên nhân cấp 3 theo NN cấp 1, 2 đã chọn
- Chỉ chọn 1 giá trị
- Bắt buộc chọn

#### Ghi chú:
- Nhập thông tin ghi chú
- Bắt buộc nhập

#### Ngày hẹn thanh toán:
- Chọn ngày hẹn, chọn giờ hẹn. Mặc định ban đầu chọn ngày hẹn
- Chọn ngày mới hiện giờ hẹn
- Chỉ chọn từ ngày hiện tại trở về sau. Không chọn ngày quá khứ

#### Ngày dự kiến khóa cước (Chỉ hiển thị đối với Thu cước):

**Khung đầu tiên:**
- Nếu không chọn thì để trống, không hiển thị khung 2,3
- Nếu chọn nội dung "Mục 2: Khóa sau mục 1 và đến cuối tháng khóa hết" ⇒ Hiển thị khung thứ 2

**Khung thứ 2:**
- Chọn "Hủy lịch khóa" hoặc chọn ngày dự kiến khóa
- Nếu chọn "Hủy lịch khóa" ⇒ Không hiển thị khung thứ 3
- Nếu chọn ngày: Bắt đầu từ ngày 13 đến cuối tháng và không cho phép chọn ngày khóa nhỏ hơn hoặc bằng ngày hiện tại

**Khung thứ 3:**
- Chọn 1 giá trị: Duy trì hoặc Tạm thời
- Bắt buộc chọn trạng thái khi chọn ngày khóa

### 3.2.3 Business Rules

#### Validation Rules:
- Ngày khóa cước nhỏ hơn ngày 13 hoặc ngày hiện tại lớn hơn hoặc bằng ngày khóa cước ⇒ Hiển thị thông báo "Thao tác thất bại. Chỉ cho phép cập nhật lịch khóa từ ngày 13 đến cuối tháng và không cho phép chọn ngày khóa nhỏ hơn hoặc bằng ngày hiện tại."

#### Data Integration:
- Lưu thông tin hợp đồng trả lý do không thanh toán
- Cập nhật bộ nguyên nhân ngày hẹn thanh toán, ngày khóa cước về tool QL Công nợ DVKH/Quản Lý Khách Hàng/Chăm sóc khách hàng
- "Kênh liên hệ" = MobiX
- "Lịch/Giờ hẹn thanh toán", "Chọn/Ngày khóa cước/Trạng thái" = Theo thông tin chọn trên mobiX
- "Ghi chú kết quả care" = ghi chú trong mục trả lý do trên mobiX

### 3.2.4 Xem lịch sử trả lý do

**Xem lịch sử trả lý do của hợp đồng trong tháng hiện tại:**
- Ngày trả lý do
- Acct trả lý do
- Nguyên nhân 1, 2, 3
- Ghi chú
- Ngày hẹn thanh toán (Lấy ngày hẹn trên tool QL Công nợ DVKH/Quản Lý Khách Hàng/Chăm sóc khách hàng)
- Ngày dự kiến khóa cước (Hiển thị đối với Thu cước, lấy thông tin trên tool Chăm sóc khách hàng)

---

## 3.3 Xem hạn mức thanh toán

### 3.3.1 Use Case Overview

| Field | Value |
|-------|--------|
| **Description** | Cho phép người dùng xem hạn mức thanh toán tạm |
| **Actor** | TIN/PNC, Thu cước |
| **Trigger** | Nhấn xem hạn mức thanh toán |
| **Pre-condition** | - Đăng nhập app thành công<br/>- Tài khoản được cấp hạn mức |
| **Post-condition** | Xem hạn mức thanh toán thành công |

### 3.3.2 Business Rules

**Hạn mức thanh toán hiển thị thông tin:**

- **Hạn mức được cấp** = Số tiền hạn mức được cấp thanh toán + Số tiền HMBS (nếu có)
- **Hạn mức sử dụng** = Tổng số tiền đã thanh toán tạm thành công  
- **Hạn mức còn lại** = Hạn mức được cấp – Hạn mức sử dụng

### 3.3.3 Example Scenario

**Ví dụ về Cấp HMBS:**

**Ngày 30/10 - Thông tin hạn mức:**
- Hạn mức được cấp = 5tr (HM chính nhân sự) + 8tr (HMBS) = 13tr
- Hạn mức sử dụng = 8tr
- Hạn mức còn lại = 5tr

**Ngày 1/11 chưa gạch nợ - Thông tin hạn mức:**
- Hạn mức được cấp = 5tr (HM chính nhân sự)
- Hạn mức sử dụng = 8tr
- Hạn mức còn lại = -3tr

---

## 3.4 Liên kết ví/Ngân hàng

### 3.4.1 Use Case Overview

| Field | Value |
|-------|--------|
| **Description** | Cho phép người dùng Liên kết hoặc hủy liên kết ví hoặc ngân hàng |
| **Actor** | TIN/PNC, Thu cước |
| **Trigger** | Nhấn chức năng Phương thức thanh toán |
| **Pre-condition** | Đăng nhập app thành công |
| **Post-condition** | Liên kết/Hủy liên kết ví hoặc ngân hàng thành công |

### 3.4.2 Screen Flow

#### Màn hình Phương thức thanh toán

**Ví FPT Pay:**

**Tài khoản Chưa liên kết:**
- Nếu nhân sự chưa cài app ⇒ Nhấn vào nút FPT pay hiển thị thông báo "Tài khoản của bạn chưa liên kết ví FPT Pay. Vui lòng tải và cài đặt FPT Pay trên cửa hàng ứng dụng và thực hiện liên kết ví"
- Nếu nhân sự đã cài app ⇒ Nhấn vào nút FPT Pay hiển thị màn hình đăng nhập app Ví FPT Pay

**Tài khoản Đã liên kết:**
- Nhấn nút Ví FPT ⇒ Hiển thị thông tin TK liên kết Ví FPT Pay

#### Màn hình Tài khoản thanh toán

**Hiển thị các thông tin:**
- Họ tên nhân sự
- Email: Email nhân sự
- Mã nhân viên: Mã nhân viên của nhân sự
- Số điện thoại: SĐT liên kết

**Nút hủy liên kết:**
- Nhấn nút Hủy liên kết hiển thị thông báo "Bạn có chắc chắn muốn hủy liên kết Ví FPT Pay không?"
- Nhấn nút Đồng ý: Hệ thống thực hiện hủy liên kết
- Nhấn Đóng: Không thực hiện hủy liên kết. Hiển thị màn hình Thông tin nhân sự

---

## 3.5 Thiết lập gửi tin nhắn

### 3.5.1 Use Case Overview

| Field | Value |
|-------|--------|
| **Description** | - Cho phép người dùng thiết lập tin nhắn gửi qua kênh nào khi thanh toán<br/>- Cho phép người dùng xem hạn mức gửi tin SMS/ZNS |
| **Actor** | TIN/PNC, CUS |
| **Trigger** | Nhấn Thiết lập gửi tin nhắn |
| **Pre-condition** | - Đăng nhập app thành công<br/>- Tài khoản được cấp gửi tin nhắn |
| **Post-condition** | - Thiết lập gửi tin nhắn thành công<br/>- Xem hạn mức gửi tin nhắn thành công |

### 3.5.2 Business Rules

#### Thiết lập gửi tin nhắn:

**Gửi qua HiFPT:**
- Đối với nhân sự thu cước mặc định gửi qua HiFPT
- Hệ thống mặc định ON nút gửi qua HiFPT, không cho chuyển tình trạng

**Gửi qua Zalo/SMS:**
- Đối với nhân sự Thu cước: Mặc định gửi qua Zalo nếu thất bại sẽ gửi SMS
- Cho phép On cả 2 kênh HiFPT và Zalo/SMS
- Đối với Gửi qua kênh HiFPT: Hệ thống sẽ gửi đến tất cả SĐT của khách hàng đã cài HiFPT
- Đối với Gửi qua kênh Zalo/SMS: Hệ thống sẽ gửi đến khách hàng bằng SĐT đã chọn tại màn hình

**Lưu ý về thiết lập:**
- Nếu nhân sự chọn gửi tin nhắn qua Zalo/SMS chỉ áp dụng đối với hợp đồng đang thiết lập
- Đối với các hợp đồng khác mặc định gửi qua HiFPT nếu như không thiết lập lại gửi Zalo/SMS
- Qua tháng sau, HĐ đã thiết lập gửi qua Zalo/SMS trước đó sẽ chuyển tình trạng về OFF

#### Hạn mức gửi Zalo/SMS:
- **Số lượng tin cấp:** Số lượng quota cấp ban đầu: 20% hợp đồng PC đầu tháng + Hạn mức cấp thêm trên Inside
- **Số lượng sử dụng:** Số lượng tin nhắn qua Zalo/SMS
- **Số lượng còn lại** = Số lượng tin cấp – Số lượng sử dụng

#### Số điện thoại:
- Load danh sách SĐT của hợp đồng. Hiển thị SĐT nhắn tin và SĐT chính chủ
- Nếu SĐT có cài HiFPT sẽ hiển thị icon nhận diện

**Trường hợp: Gửi qua HiFPT, Không gửi qua Zalo/SMS:**
- SĐT có cài HiFPT sẽ mặc định check chọn, không có bỏ check

**Trường hợp: Gửi qua HiFPT và Zalo/SMS:**
- Chỉ chọn 1 SĐT
- Mặc định check vào SĐT chính chủ

### 3.5.3 Message Templates

#### Template SMS Kỹ thuật:
```
"FPT Telecom thong bao: So tien Quy khach thanh toan cho HÐ SGFDN1015 la 55000 VND. Xin cam on. (ISC01.TRANGPT30)"
```

#### Template SMS Thu cước:
```
"Cam on ban da thanh toan thanh cong so 200,000d, so chung tu: U23SG0073526 tu ngay 01/06/2025 – 30/06/2025 cua hop dong SGH236501. LH 19006600"
```

**Lưu ý:** 1 mẫu SMS tương ứng cho 1 hóa đơn hoặc khoản thu, nếu thanh toán 5 hóa đơn sẽ gửi SMS 5 lần.

#### Template Zalo Thu cước:
Nội dung template ZNS thanh toán hóa đơn, khoản thu. 1 mẫu ZNS tương ứng cho 1 hóa đơn hoặc khoản thu.

---

## 3.6 Thanh toán hợp đồng đại diện

### 3.6.1 Use Case Overview

| Field | Value |
|-------|--------|
| **Description** | Cho phép người dùng xem và thanh toán hợp đồng đại diện |
| **Actor** | TIN/PNC, Thu cước |
| **Trigger** | Nhấn Thanh toán HDDD |
| **Pre-condition** | Đăng nhập app thành công |
| **Post-condition** | Thanh toán HDDD thành công |

### 3.6.2 Screen Layout

#### Màn hình danh sách HDDD

**Tab Tất cả:**
- Hiển thị tất cả HDDD Chưa thanh toán, Đã thanh toán
- Sắp xếp: "Chưa thanh toán" và TG tạo HDDD từ xa đến gần ⇒ "Đã thanh toán" và TG tạo HDDD từ gần đến xa

**Tab Đã thanh toán:**
- Load tất cả HDDD đã thanh toán
- Mặc định ban đầu D, D-1, D-2 (D là ngày)
- Sắp xếp: Trạng thái "Đã thanh toán" có ngày tạo HDDD từ gần đến xa

**Tab Chưa thanh toán:** (Mặc định ban đầu khi chọn chức năng Quản lý Công nợ)
- Load tất cả HDDD Chưa thanh toán
- Mặc định ban đầu T, T-1, T-2 (T là tháng hiện tại)
- Sắp xếp: Trạng thái "Chưa thanh toán" có ngày tạo HDDD xa đến gần

#### Danh sách hợp đồng đại diện

**Nút Chọn tất cả:**
- Check Chọn tất cả
- Mặc định ban đầu uncheck
- Nút Chọn Tất cả ẩn đi khi ở tab Đã thanh toán và Tab Tất cả khi không có HDDD chưa thanh toán

**Thông tin HDDD:**
- **Nút chọn HDDD:** 
  - Nếu tình trạng HDDD = "Chưa thanh toán" ⇒ Hiển thị nút check chọn
  - Nếu tình trạng HDDD = "Đã thanh toán" ⇒ Ẩn nút check
- **SHĐ:** Hiển thị số HDDD
- **Thời gian tạo:** Hiển thị thời gian thanh toán nhỏ nhất trong danh sách của HĐ con
- **TG nộp tiền:** Hiển thị thời gian thanh toán HDDD. Nếu HĐ trạng thái "Chưa thanh toán" sẽ ẩn đi
- **Số tiền:** Sum tổng tiền tất cả HĐ con thuộc HDDD
- **Phương thức thanh toán:** 
  - Nếu HDDD chưa thanh toán: ẩn thông tin
  - Nếu HDDD đã thanh toán: Hiển thị PTTT HDDD
- **Tình trạng:** Chưa thanh toán, Đã thanh toán
- **Nút xem chi tiết:** Hiển thị màn hình chi tiết Công nợ với tổng số HDDD con thuộc HDDD

#### Tổng tiền:
- Nếu trong danh sách có HDDD Chưa thanh toán: Tổng số tiền HDDD được check chọn (Nếu chưa check HDDD nào hiển thị 0đ)
- Nếu trong danh sách không có HDDD Chưa thanh toán: Sum tổng tiền các HDDD đang hiển thị

#### Nút thanh toán:
- Nếu trong danh sách có HDDD Chưa thanh toán: Hiển thị nút thanh toán
- Nếu trong danh sách không có HDDD Chưa thanh toán: Nút thanh toán mờ đi, không cho thao tác

### 3.6.3 Filter & Search

**Bộ lọc tìm kiếm:**

#### Trạng thái thanh toán:
- Tất cả
- Chưa thanh toán
- Đã thanh toán
- Mặc định ban đầu không chọn giá trị nào
- Chỉ chọn 1 giá trị

#### Thời gian: (lọc theo TG tạo HDDD trong phạm vi T,T-1,T-2)
- **Hôm nay:** lọc ngày hiện tại
- **7 ngày gần nhất:** Từ ngày hiện tại trở trước. Trong phạm vi 7 ngày
- **Khoảng thời gian:** Chọn Từ ngày Đến ngày (chỉ chọn trong phạm vi 3 tháng gần nhất)

#### Tìm kiếm theo:
- **Hợp đồng đại diện:** Tìm kiếm theo số hợp đồng đại diện
- **Số hợp đồng:** Tìm kiếm theo số hợp đồng con (Hợp đồng của khách hàng)

### 3.6.4 Detail Screens

#### Chi tiết Công nợ:
**Hiển thị các thông tin:**
- Số hợp đồng đại diện
- **Danh sách hợp đồng con:**
  - Nút check chọn HDDD
  - Số hợp đồng con
  - Số tiền: Tổng số tiền đã thanh toán của HĐ con
- **Nút thanh toán:**
  - Nếu HDDD trạng thái Đã thanh toán ⇒ Mờ đi nút thanh toán, không cho thao tác
  - Nếu HDDD trạng thái chưa thanh toán ⇒ Hiển thị nút thanh toán
  - Thanh toán thành công, reload lại màn hình chi tiết công nợ. Hiển thị ở tab Đã thanh toán

#### Chi tiết công nợ của hợp đồng:
**Hiển thị các thông tin:**
- Số hợp đồng con
- Tổng tiền: Tổng tiền các khoản đã thanh toán
- **Danh sách các khoản đã thanh toán:**
  - Khách hàng: Tên khách hàng
  - Hóa đơn/Khoản thu: Số hóa đơn/Khoản thu
  - TG thu tiền: Thời gian thu tiền HĐ con
  - Số tiền: Số tiền đã thanh toán

### 3.6.5 Payment Process

#### Nhấn Thanh toán:

**Validation Rules:**
- Nhấn thanh toán nếu chưa check HDDD nào ⇒ Hiển thị thông báo "Vui lòng chọn HDDD cần thanh toán"
- Chỉ được chọn tối đa 5 HDDD cần thanh toán ⇒ Nếu chọn quá 5 khoản hiển thị thông báo "Chỉ được chọn tối đa 5 HDDD thanh toán"
- Thanh toán HDDD xa nhất trước: Nếu tích chọn HDDD có ngày tạo lớn hơn ngày tạo của các HDDD còn lại chưa tích chọn ⇒ Hiển thị thông báo "Vui lòng thanh toán HDDD xa nhất"

#### Màn hình chọn PTTT:

**Ví FPT Pay:**
- Nếu chưa liên kết ví ⇒ Nhấn Tiếp tục hiển thị thông báo "Vui lòng thực hiện liên kết phương thức thanh toán"
- Nếu đã liên kết ví ⇒ Hiển thị màn hình nhập mã OTP hoặc mật khẩu để thanh toán
- Thanh toán thành công, reload lại màn hình danh sách HDDD và hiển thị Tab Đã thanh toán

**Mã QR:**
- Hiển thị mã QR thanh toán cho các HDDD đã chọn
- **Lưu mã:** Tải ảnh QR về máy
- Mã QR thanh toán được trên các app ngân hàng và ví điện tử
- **Thanh toán thành công:**
  - Gạch nợ HDDD
  - Reload lại màn hình chi tiết công nợ. Hiển thị ở tab Đã thanh toán

---

# 4. DOCUMENT STRUCTURE & OWNERSHIP

## 4.1 Document Responsibility Matrix

| STT | Hạng mục | Phụ trách | Ghi chú |
|-----|----------|-----------|---------|
| A | GIỚI THIỆU | PO, BA | Giới thiệu các thông tin chung của dự án |
| B | TỔNG QUAN | BA, PIC | Mô tả tổng quan thông tin của Product |
| C | ĐẶC TẢ CÁC CHỨC NĂNG | BA, PIC | Đặc tả chi tiết các chức năng<br/>Báo cáo, Notification list, Message list, Email template: có thể customize lại gom vào từng chức năng |

---

# 5. ANALYSIS SUMMARY

## 5.1 Document Overview

This URD document for **Mobinet Nextgen VER 2.0** provides comprehensive requirements for a payment SDK system designed to serve Sales, TIN/PNC, and debt collection staff. The system focuses on bill payment and fee collection functionalities with multiple payment methods and notification channels.

## 5.2 Key Features Analysis

### Core Payment Functions:
1. **Payment Processing** - Main payment interface with comprehensive validation rules
2. **Non-payment Reason Tracking** - Detailed reason classification and follow-up scheduling  
3. **Payment Limit Management** - Real-time limit monitoring and tracking
4. **Wallet/Bank Linking** - Integration with FPT Pay and banking systems
5. **Notification Setup** - Multi-channel notification configuration (HiFPT, Zalo, SMS)
6. **Representative Contract Payment** - Batch payment processing for representative contracts

### Business Logic Complexity:
- **Advanced validation rules** for different user types (TIN/PNC vs Debt Collection)
- **Multi-tier payment method support** (Cash, FPT Pay, QR codes)
- **Sophisticated notification routing** based on app installation and user preferences
- **Complex limit management** including supplementary limits and carryover rules
- **Comprehensive audit trail** for all payment activities

### Technical Integration Points:
- **FPT Pay Wallet System** - Deep integration for payment processing
- **VN Pay QR System** - QR code generation and validation
- **HiFPT App Integration** - Notification delivery to installed apps
- **Zalo/SMS Gateway** - Fallback notification channels
- **Internal Tools Integration** - Data synchronization with customer care and debt management tools

## 5.3 User Personas

### Primary Users:
1. **TIN/PNC Staff** - Technical installation and customer service personnel
2. **Debt Collection Staff** - Specialized in payment collection and follow-up
3. **Sales Staff** - Customer-facing payment collection

### User Journey Complexity:
- **Multi-step payment flows** with extensive validation
- **Context-aware interface behavior** based on user role and contract type
- **Comprehensive error handling** with detailed user feedback
- **Flexible payment method selection** based on user preferences and capabilities

## 5.4 System Architecture Implications

### Key Architectural Considerations:
1. **Real-time Payment Processing** - Immediate validation and confirmation
2. **Multi-system Integration** - Coordination with multiple external systems
3. **Role-based Access Control** - Different features and rules per user type
4. **Notification Orchestration** - Intelligent routing across multiple channels
5. **Audit and Compliance** - Comprehensive logging for financial transactions
6. **Mobile-first Design** - Optimized for field staff mobile usage

## 5.5 Implementation Complexity Assessment

### High Complexity Areas:
- **Payment Rule Engine** - Complex business rules with multiple conditions
- **Multi-channel Notifications** - Sophisticated routing and delivery tracking
- **Limit Management System** - Real-time calculations with carryover logic
- **Integration Orchestration** - Coordination between multiple external systems
- **Mobile Payment UX** - Seamless payment flows across different methods

### Medium Complexity Areas:
- **User Interface Design** - Multiple screens with conditional visibility
- **Data Synchronization** - Keeping multiple systems in sync
- **Error Handling** - Comprehensive error scenarios and recovery

### Development Recommendations:
1. **Phase Implementation** - Start with core payment flows, add advanced features incrementally
2. **Extensive Testing** - Payment systems require comprehensive testing including edge cases
3. **Security Focus** - Financial data handling requires robust security measures
4. **Performance Optimization** - Mobile users need fast, responsive interfaces
5. **Integration Strategy** - Plan careful integration testing with all external systems

## 5.6 Success Metrics

Based on the requirements, success should be measured by:
- **Payment Processing Accuracy** - Zero payment errors
- **User Adoption Rate** - Staff usage across all target personas
- **Payment Method Coverage** - Support for all required payment types
- **Notification Delivery Rate** - Successful message delivery across all channels
- **System Integration Reliability** - Seamless data flow between systems
- **Mobile Performance** - Fast, responsive mobile interface

---

**Document Generation Information:**
- **Source Document:** /Users/nguyenhuunhan/Documents/ai_project/agents/document/urd.docx
- **Processing Date:** 2025-09-09
- **Document Processor:** Python Document Processor v1.0
- **Content Extracted:** 75 paragraphs, 19 tables
- **Analysis Depth:** Comprehensive structural and functional analysis

---

**Wireframe Reference Links:**
- [Main Design System](https://www.figma.com/design/Ex8yecMU7ZfmHpYurQQRwW/MBX-T%C3%ADch-h%E1%BB%A3p?node-id=81-2734&t=58y2YFKmjccJFd57-1)