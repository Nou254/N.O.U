import { configureStore } from '@reduxjs/toolkit'
import authReducer from './authSlice'
import productReducer from './productSlice'
import assessmentReducer from './assessmentSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    products: productReducer,
    assessment: assessmentReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
})

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch