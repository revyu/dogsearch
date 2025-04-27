import { QueryClient } from '@tanstack/react-query';

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60_000,       // 1 минута: список собак не устаревает каждую секунду
      retry: 1,                // одна повторная попытка при ошибке
    },
  },
});