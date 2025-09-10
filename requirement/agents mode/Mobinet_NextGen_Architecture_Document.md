# Mobinet NextGen Ver 2.0 - Architecture Document

## 1. Executive Summary

### 1.1 Project Overview
**System Name:** Mobinet NextGen Ver 2.0  
**Organization:** FPT Telecom  
**Document Version:** 1.0  
**Date:** 2025-01-10  

### 1.2 Purpose
This document defines the technical architecture for Mobinet NextGen Ver 2.0, a comprehensive payment SDK designed to modernize bill and fee payment processing for FPT Telecom's sales, technical installation/post-care (TIN/PNC), and revenue collection operations.

### 1.3 Scope
The architecture encompasses mobile SDK development, payment gateway integrations, notification systems, and backend services supporting 1000+ concurrent users with 10,000+ transactions per hour capacity.

## 2. System Architecture Overview

### 2.1 Architecture Pattern
The system follows a **Microservices Architecture** with the following key principles:
- **Mobile-First Design**: Native iOS/Android SDK with offline capabilities
- **API-Driven**: RESTful services with JWT authentication
- **Event-Driven**: Asynchronous processing for notifications and audit trails
- **Multi-Tenant**: Support for different user roles and organizational units

### 2.2 High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  Mobile Apps (iOS/Android)  │  Web Portal  │  Admin Dashboard    │
│  - Payment Interface        │  - Reports   │  - Configuration    │
│  - Offline Capability       │  - Analytics │  - User Management  │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API GATEWAY LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  API Gateway (Kong/AWS API Gateway)                             │
│  - Authentication & Authorization                               │
│  - Rate Limiting & Throttling                                   │
│  - Request/Response Transformation                              │
│  - Monitoring & Logging                                         │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   BUSINESS SERVICES LAYER                       │
├─────────────────────────────────────────────────────────────────┤
│ Payment Service │ Notification │ Non-Payment  │ Limit Management │
│ - Process Bills │ Service      │ Reason Mgmt  │ Service          │
│ - Handle Fees   │ - SMS/Zalo   │ - Reason     │ - Daily Limits   │
│ - Multi-Gateway │ - Push Notif │   Tracking   │ - Role Limits    │
│ - Validation    │ - Email      │ - Reporting  │ - Validation     │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                   INTEGRATION LAYER                             │
├─────────────────────────────────────────────────────────────────┤
│ Payment Gateways │ External APIs │ Internal Systems             │
│ - FPT Pay       │ - SMS Gateway │ - Revenue Management         │
│ - VN Pay        │ - Zalo API    │ - Customer Management        │
│ - Banking APIs  │ - Email SMTP  │ - HiFPT Platform            │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DATA LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│ Primary Database │ Cache Layer  │ Message Queue │ File Storage   │
│ - PostgreSQL     │ - Redis      │ - RabbitMQ    │ - AWS S3       │
│ - Transactions   │ - Sessions   │ - Events      │ - Documents    │
│ - Master Data    │ - Lookups    │ - Async Jobs  │ - Reports      │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Component Architecture

### 3.1 Mobile SDK Architecture

#### 3.1.1 Core Components
```
Mobile SDK
├── Authentication Module
│   ├── JWT Token Management
│   ├── Biometric Authentication
│   └── Session Management
├── Payment Processing Module
│   ├── Payment Gateway Integration
│   ├── Transaction Validation
│   ├── Offline Transaction Queue
│   └── Receipt Generation
├── Data Synchronization Module
│   ├── Offline Data Storage
│   ├── Sync Manager
│   └── Conflict Resolution
├── Notification Module
│   ├── Push Notification Handler
│   ├── In-App Messaging
│   └── Notification History
└── Security Module
    ├── Data Encryption
    ├── Certificate Pinning
    └── Anti-Tampering Protection
```

#### 3.1.2 Offline Capability Design
- **Local SQLite Database**: Store transaction data for offline processing
- **Sync Queue**: Queue transactions when offline, sync when online
- **Conflict Resolution**: Handle concurrent modifications during sync
- **Data Integrity**: Ensure consistency between local and remote data

### 3.2 Backend Services Architecture

#### 3.2.1 Payment Service
```yaml
Payment Service:
  Components:
    - Payment Controller
    - Payment Processor
    - Gateway Manager
    - Transaction Validator
    - Receipt Generator
  
  External Integrations:
    - FPT Pay API
    - VN Pay API
    - Banking APIs
  
  Data Models:
    - PaymentTransaction
    - PaymentMethod
    - TransactionStatus
    - Receipt
```

#### 3.2.2 Notification Service
```yaml
Notification Service:
  Components:
    - Notification Controller
    - Message Queue Processor
    - Channel Manager
    - Template Engine
    - Delivery Status Tracker
  
  Channels:
    - SMS (Quota-based)
    - Zalo Business API
    - Push Notifications
    - Email
  
  Features:
    - Message Templating
    - Personalization
    - Delivery Tracking
    - Retry Mechanisms
```

#### 3.2.3 Non-Payment Reason Management
```yaml
Non-Payment Reason Service:
  Components:
    - Reason Controller
    - Classification Engine
    - Analytics Processor
    - Report Generator
  
  Features:
    - Automated Reason Detection
    - Manual Reason Assignment
    - Statistical Analysis
    - Trend Reporting
```

#### 3.2.4 Payment Limit Management
```yaml
Limit Management Service:
  Components:
    - Limit Controller
    - Validation Engine
    - Policy Manager
    - Usage Tracker
  
  Limit Types:
    - Daily Payment Limits
    - Role-based Limits
    - Customer Category Limits
    - Geographic Limits
```

## 4. Technology Stack

### 4.1 Mobile Development
- **iOS**: Swift 5.0+, iOS 12.0+
- **Android**: Kotlin, Android API Level 23+
- **Cross-Platform Considerations**: Native development for optimal performance
- **Local Storage**: SQLite for offline data
- **Security**: Keychain (iOS), Keystore (Android)

### 4.2 Backend Development
- **Runtime**: Node.js 18+ or Java 17+
- **Framework**: Express.js or Spring Boot
- **API**: RESTful with OpenAPI 3.0 specification
- **Authentication**: JWT with refresh token mechanism
- **Validation**: Schema-based validation (JSON Schema/Bean Validation)

### 4.3 Database & Storage
- **Primary Database**: PostgreSQL 14+
- **Cache**: Redis 6+
- **Message Queue**: RabbitMQ or AWS SQS
- **File Storage**: AWS S3 or compatible object storage
- **Search**: Elasticsearch (for analytics)

### 4.4 Infrastructure
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **API Gateway**: Kong or AWS API Gateway
- **Load Balancer**: HAProxy or AWS ALB
- **Monitoring**: Prometheus + Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)

## 5. Security Architecture

### 5.1 Security Layers

#### 5.1.1 Application Security
- **Authentication**: Multi-factor authentication (MFA)
- **Authorization**: Role-Based Access Control (RBAC)
- **Data Validation**: Input sanitization and validation
- **Session Management**: Secure session handling with timeout
- **API Security**: Rate limiting and DDoS protection

#### 5.1.2 Data Security
- **Encryption at Rest**: AES-256 encryption for sensitive data
- **Encryption in Transit**: TLS 1.3 for all communications
- **Key Management**: Hardware Security Module (HSM) or AWS KMS
- **Data Masking**: Sensitive data masking in logs and reports
- **PII Protection**: Personal data anonymization and pseudonymization

#### 5.1.3 Network Security
- **VPC/VLAN Segmentation**: Network isolation
- **Firewall Rules**: Strict ingress/egress controls
- **Certificate Management**: Automated certificate lifecycle
- **VPN Access**: Secure administrative access
- **WAF Protection**: Web Application Firewall

### 5.2 Compliance Requirements
- **PCI DSS**: Payment card industry compliance
- **Vietnamese Data Protection**: Local data protection regulations
- **Audit Trail**: Comprehensive logging of all transactions
- **Data Retention**: Automated data lifecycle management

## 6. Performance & Scalability

### 6.1 Performance Requirements
- **Transaction Processing**: < 30 seconds end-to-end
- **Data Loading**: < 5 seconds for standard queries
- **Concurrent Users**: 1000+ simultaneous active users
- **Transaction Volume**: 10,000+ transactions per hour
- **Availability**: 99.9% uptime during business hours

### 6.2 Scalability Design
- **Horizontal Scaling**: Stateless service design
- **Database Sharding**: Partition large tables by customer/region
- **Caching Strategy**: Multi-level caching (Application, Database, CDN)
- **Load Distribution**: Geographic load balancing
- **Auto-scaling**: Dynamic resource allocation based on load

### 6.3 Performance Optimization
- **Database Optimization**: Query optimization and indexing strategy
- **Connection Pooling**: Database connection management
- **Async Processing**: Non-blocking operations for heavy tasks
- **CDN Integration**: Static content delivery optimization
- **Monitoring**: Real-time performance monitoring and alerting

## 7. Integration Architecture

### 7.1 Internal System Integrations

#### 7.1.1 Revenue Management System
```yaml
Integration:
  Protocol: RESTful API
  Authentication: OAuth 2.0
  Data Format: JSON
  
Endpoints:
  - GET /api/v1/customers/{id}/bills
  - GET /api/v1/customers/{id}/fees
  - POST /api/v1/payments
  - PUT /api/v1/payments/{id}/status
```

#### 7.1.2 Customer Management System
```yaml
Integration:
  Protocol: RESTful API
  Authentication: API Key + JWT
  Data Format: JSON
  
Endpoints:
  - GET /api/v1/customers/{id}
  - GET /api/v1/customers/search
  - POST /api/v1/customers/{id}/contacts
```

#### 7.1.3 HiFPT Platform Integration
```yaml
Integration:
  Protocol: WebSocket + REST
  Authentication: JWT
  Real-time Events: WebSocket
  Data Sync: Scheduled REST calls
```

### 7.2 External Payment Gateway Integration

#### 7.2.1 FPT Pay Integration
```yaml
Integration:
  Protocol: HTTPS POST
  Authentication: API Key + Digital Signature
  Encryption: RSA-2048
  
Payment Flow:
  1. Initialize Payment Request
  2. Redirect to FPT Pay
  3. Process Payment Response
  4. Verify Transaction Status
```

#### 7.2.2 VN Pay Integration
```yaml
Integration:
  Protocol: HTTPS POST/GET
  Authentication: SHA-256 Hash
  Return URL: Configurable callback
  
Payment Methods:
  - QR Code Payment
  - Bank Transfer
  - Wallet Payment
```

### 7.3 Notification Channel Integration

#### 7.3.1 SMS Gateway
```yaml
Integration:
  Provider: Multiple providers (failover)
  Protocol: HTTP REST API
  Rate Limiting: Quota-based
  Templates: Configurable message templates
```

#### 7.3.2 Zalo Business API
```yaml
Integration:
  Protocol: HTTPS REST
  Authentication: OAuth 2.0
  Message Types:
    - Text Messages
    - Rich Media Messages
    - Transaction Updates
```

## 8. Deployment Architecture

### 8.1 Environment Strategy
```yaml
Environments:
  Development:
    - Local Docker containers
    - Mock external services
    - SQLite for development database
  
  Staging:
    - Kubernetes cluster
    - External service sandbox
    - PostgreSQL replica
  
  Production:
    - Multi-AZ Kubernetes deployment
    - Production external services
    - High-availability PostgreSQL cluster
```

### 8.2 CI/CD Pipeline
```yaml
Pipeline Stages:
  1. Code Quality:
     - Static code analysis
     - Unit tests (>80% coverage)
     - Security scanning
  
  2. Build & Package:
     - Docker image creation
     - Dependency vulnerability scan
     - Artifact versioning
  
  3. Deploy & Test:
     - Automated deployment
     - Integration tests
     - Performance tests
  
  4. Production Release:
     - Blue-green deployment
     - Health checks
     - Rollback capability
```

### 8.3 Monitoring & Observability
```yaml
Monitoring Stack:
  Metrics:
    - Prometheus for metric collection
    - Grafana for visualization
    - AlertManager for notifications
  
  Logging:
    - Centralized logging with ELK stack
    - Structured JSON logging
    - Log aggregation and analysis
  
  Tracing:
    - Distributed tracing with Jaeger
    - Performance bottleneck identification
    - Request flow visualization
  
  Health Checks:
    - Application health endpoints
    - Database connectivity checks
    - External service dependency checks
```

## 9. Data Flow Architecture

### 9.1 Payment Processing Flow
```
1. Mobile App → API Gateway → Payment Service
2. Payment Service → Payment Gateway (FPT Pay/VN Pay)
3. Payment Gateway → Bank/Wallet Provider
4. Bank/Wallet → Payment Gateway (Response)
5. Payment Gateway → Payment Service (Confirmation)
6. Payment Service → Database (Update)
7. Payment Service → Notification Service (Event)
8. Notification Service → SMS/Zalo/Push (Notify User)
9. Payment Service → Mobile App (Receipt)
```

### 9.2 Notification Flow
```
1. Business Event → Message Queue
2. Notification Service → Template Engine
3. Template Engine → Channel Manager
4. Channel Manager → External APIs (SMS/Zalo/Email)
5. Delivery Status → Database (Logging)
6. Failed Deliveries → Retry Queue
```

### 9.3 Data Synchronization Flow
```
1. Mobile App (Offline) → Local SQLite
2. Network Available → Sync Manager
3. Sync Manager → API Gateway
4. API Gateway → Business Services
5. Conflict Detection → Resolution Engine
6. Database Update → Response
7. Mobile App → Local Data Update
```

## 10. Disaster Recovery & Business Continuity

### 10.1 Backup Strategy
- **Database Backups**: Daily full backups, hourly incremental
- **Application Data**: Real-time replication to secondary region
- **Configuration Management**: Version-controlled infrastructure as code
- **Document Storage**: Cross-region replication for file storage

### 10.2 Failover Mechanisms
- **Database Failover**: Automatic primary-replica failover
- **Service Failover**: Multi-AZ deployment with health checks
- **Payment Gateway Failover**: Multiple gateway providers with routing
- **Network Failover**: Multiple ISP connections with BGP routing

### 10.3 Recovery Procedures
- **RTO (Recovery Time Objective)**: 4 hours maximum
- **RPO (Recovery Point Objective)**: 15 minutes maximum
- **Testing**: Monthly disaster recovery testing
- **Documentation**: Detailed runbooks for all recovery scenarios

## 11. Conclusion

This architecture document provides the foundation for implementing Mobinet NextGen Ver 2.0 as a scalable, secure, and performant payment processing system. The microservices-based approach ensures modularity and maintainability, while the comprehensive integration strategy supports both current and future business requirements.

The architecture addresses all functional and non-functional requirements identified in the URD, providing a roadmap for development teams to build a robust payment platform that can handle FPT Telecom's growing transaction volume and evolving business needs.

## 12. Appendices

### Appendix A: API Specifications
- RESTful API documentation with OpenAPI 3.0
- Authentication flows and token management
- Error handling and status codes
- Rate limiting and throttling policies

### Appendix B: Security Specifications
- Detailed security controls and implementations
- Threat modeling and risk assessments
- Compliance checklists and validation procedures
- Security testing and penetration testing guidelines

### Appendix C: Performance Specifications
- Detailed performance benchmarks and testing procedures
- Capacity planning and resource allocation guidelines
- Performance monitoring and alerting configurations
- Optimization techniques and best practices