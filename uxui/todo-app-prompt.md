# TODO App Design Prompt

## Nhiệm vụ (Task)
Thiết kế giao diện TODO App với trải nghiệm người dùng tối ưu và thân thiện

## Phong cách thiết kế (Design Style)
**Neobrutalism** - Phong cách thiết kế táo bạo với:
- Đường viền đậm, góc cạnh
- Bóng đổ mạnh mẽ
- Typography in đậm
- Màu sắc tương phản cao
- Layout không đối xứng, sáng tạo

## Màu sắc chủ đạo (Color Palette)
- **Vàng (#FFD700, #FFC107)**: Màu chính cho các action buttons, highlights
- **Xanh dương (#2196F3, #1976D2)**: Màu phụ cho navigation, secondary elements
- **Xanh lá (#4CAF50, #388E3C)**: Màu cho trạng thái completed, success states
- **Màu trung tính**: Đen (#000000), Trắng (#FFFFFF) cho contrast

## Font chữ (Typography)
**Variable Fonts** với đặc điểm:
- Chiều rộng mỗi ký tự bằng nhau (Monospace characteristics)
- Hỗ trợ multiple weights (Light, Regular, Medium, Bold, Black)
- Khả năng điều chỉnh linh hoạt theo context
- Ví dụ: JetBrains Mono Variable, SF Mono, Fira Code Variable

## Design Story
**Focus on Wibu Lover** - Hướng đến cộng đồng yêu thích văn hóa Anime/Manga:
- Tích hợp subtle anime-inspired elements
- Color scheme lấy cảm hứng từ anime aesthetics
- Micro-interactions mang tính playful
- Easter eggs và references cho wibu community
- Typography và iconography có chút anime vibe

## Layout Structure
### Sidebar Navigation
- **Left Menu**: Danh sách các projects
- Sticky position với scroll independent
- Collapse/expand functionality
- Quick project switching

### Main Container
- **Task Display Area**: Hiển thị danh sách tasks của project được chọn
- Responsive grid/list layout
- Filter và sort options
- Search functionality

## Micro Animations & Effects

### Hover Effects
- Button scale và color transition
- Card lift effect với shadow animation
- Icon rotation/bounce effects
- Subtle glow effects

### Click Interactions
- Ripple effect on buttons
- Checkbox animation với spring physics
- Task completion slide-out animation
- Loading states với skeleton screens

### Transition Effects
- Smooth page transitions
- Stagger animations cho task lists
- Parallax scrolling elements
- Morphing icons và shapes

## Special Effects

### Confetti Effect
**Trigger**: Khi hoàn thành task
- **Animation**: Colorful confetti falling từ trên xuống
- **Duration**: 2-3 seconds
- **Colors**: Sử dụng color palette chính (vàng, xanh dương, xanh lá)
- **Physics**: Realistic gravity và wind effects
- **Sound**: Optional celebratory sound effect

### Additional Interactions
- Progress bar animations
- Celebration particles cho milestones
- Subtle background animations
- Themed seasonal effects (optional)

## Technical Considerations
- Mobile-first responsive design
- Dark/Light mode support
- Accessibility compliance (WCAG 2.1)
- Performance optimization cho animations
- Cross-browser compatibility
- PWA capabilities

## User Experience Goals
- Tạo cảm giác vui vẻ và động lực khi sử dụng
- Giảm thiểu cognitive load
- Tăng engagement thông qua gamification elements
- Phù hợp với aesthetic preferences của wibu community
- Smooth và intuitive workflow
