import { create } from 'zustand';
import { devtools } from 'zustand/middleware';
import { 
  NonPaymentReasonState, 
  NonPaymentReason, 
  NonPaymentReasonFormData,
  NonPaymentHistory,
  ValidationError,
  UserRole 
} from '@/types/nonPaymentReason';

interface NonPaymentReasonActions {
  // Reason management
  setLevel1Reasons: (reasons: NonPaymentReason[]) => void;
  setLevel2Reasons: (reasons: NonPaymentReason[]) => void;
  setLevel3Reasons: (reasons: NonPaymentReason[]) => void;
  loadReasonsLevel2: (level1Id: string) => Promise<void>;
  loadReasonsLevel3: (level1Id: string, level2Id: string) => Promise<void>;
  
  // Form management
  updateFormData: (data: Partial<NonPaymentReasonFormData>) => void;
  resetForm: () => void;
  setErrors: (errors: ValidationError[]) => void;
  clearErrors: () => void;
  
  // History management
  setHistory: (history: NonPaymentHistory[]) => void;
  loadHistory: (contractId: string) => Promise<void>;
  
  // User management
  setCurrentUser: (user: UserRole) => void;
  
  // Loading states
  setLoading: (loading: boolean) => void;
  
  // Actions
  submitForm: () => Promise<boolean>;
}

const initialFormData: NonPaymentReasonFormData = {
  reasonLevel1: '',
  reasonLevel2: '',
  reasonLevel3: '',
  note: '',
  appointmentDate: new Date(),
  appointmentTime: '09:00',
  lockDate: undefined,
  lockStatus: 'maintain',
  lockOption: 'none'
};

export const useNonPaymentReasonStore = create<NonPaymentReasonState & NonPaymentReasonActions>()(
  devtools(
    (set, get) => ({
      // Initial state
      reasons: {
        level1: [],
        level2: [],
        level3: []
      },
      formData: initialFormData,
      history: [],
      isLoading: false,
      errors: [],
      currentUser: null,

      // Reason management actions
      setLevel1Reasons: (reasons) => set({ 
        reasons: { ...get().reasons, level1: reasons } 
      }),
      
      setLevel2Reasons: (reasons) => set({ 
        reasons: { ...get().reasons, level2: reasons, level3: [] } 
      }),
      
      setLevel3Reasons: (reasons) => set({ 
        reasons: { ...get().reasons, level3: reasons } 
      }),

      loadReasonsLevel2: async (level1Id: string) => {
        set({ isLoading: true });
        try {
          // API call to load level 2 reasons
          const response = await fetch(`/api/non-payment-reasons/level2?level1=${level1Id}`);
          const reasons = await response.json();
          
          set({ 
            reasons: { ...get().reasons, level2: reasons, level3: [] },
            formData: { ...get().formData, reasonLevel2: '', reasonLevel3: '' }
          });
        } catch (error) {
          console.error('Error loading level 2 reasons:', error);
        } finally {
          set({ isLoading: false });
        }
      },

      loadReasonsLevel3: async (level1Id: string, level2Id: string) => {
        set({ isLoading: true });
        try {
          // API call to load level 3 reasons
          const response = await fetch(`/api/non-payment-reasons/level3?level1=${level1Id}&level2=${level2Id}`);
          const reasons = await response.json();
          
          set({ 
            reasons: { ...get().reasons, level3: reasons },
            formData: { ...get().formData, reasonLevel3: reasons.length > 0 ? '' : undefined }
          });
        } catch (error) {
          console.error('Error loading level 3 reasons:', error);
          set({ reasons: { ...get().reasons, level3: [] } });
        } finally {
          set({ isLoading: false });
        }
      },

      // Form management actions
      updateFormData: (data) => set({ 
        formData: { ...get().formData, ...data } 
      }),
      
      resetForm: () => set({ 
        formData: initialFormData,
        errors: [],
        reasons: { ...get().reasons, level2: [], level3: [] }
      }),
      
      setErrors: (errors) => set({ errors }),
      
      clearErrors: () => set({ errors: [] }),

      // History management actions
      setHistory: (history) => set({ history }),
      
      loadHistory: async (contractId: string) => {
        set({ isLoading: true });
        try {
          const response = await fetch(`/api/non-payment-history?contractId=${contractId}`);
          const history = await response.json();
          set({ history });
        } catch (error) {
          console.error('Error loading history:', error);
          set({ history: [] });
        } finally {
          set({ isLoading: false });
        }
      },

      // User management actions
      setCurrentUser: (user) => set({ currentUser: user }),
      
      // Loading state actions
      setLoading: (loading) => set({ isLoading: loading }),

      // Submit form action
      submitForm: async () => {
        const { formData, currentUser } = get();
        set({ isLoading: true, errors: [] });
        
        try {
          const response = await fetch('/api/non-payment-reasons/submit', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              ...formData,
              staffAccount: currentUser?.account
            })
          });

          if (!response.ok) {
            const errorData = await response.json();
            set({ errors: errorData.errors || [] });
            return false;
          }

          // Success - reload history
          if (currentUser) {
            await get().loadHistory(formData.reasonLevel1); // Use contract ID in real implementation
          }
          
          get().resetForm();
          return true;
        } catch (error) {
          console.error('Error submitting form:', error);
          set({ errors: [{ field: 'general', message: 'Có lỗi xảy ra khi cập nhật' }] });
          return false;
        } finally {
          set({ isLoading: false });
        }
      }
    }),
    {
      name: 'non-payment-reason-store'
    }
  )
);