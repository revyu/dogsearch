import React from 'react';
import { View, Panel, PanelSpinner, Div } from '@vkontakte/vkui';
import {
  useRouteNavigator,
  useActiveVkuiLocation,
  useMetaParams,
} from '@vkontakte/vk-mini-apps-router';
import { useQuery } from '@tanstack/react-query';

import { DEFAULT_VIEW_PANELS } from './routes';
import { AnimalList } from './components/AnimalList';
import { AnimalCard } from './components/AnimalCard';
import { getAnimals } from './shared/api';
import type { AnimalSummary } from './components/AnimalList';

export const App: React.FC = () => {
  const navigator = useRouteNavigator();
  const { panel }   = useActiveVkuiLocation();
  const { id }      = useMetaParams<{ id?: string }>() ?? {};

  const activePanel = panel || DEFAULT_VIEW_PANELS.HOME;

  // Для списка животных
  const { data: animals = [], isLoading: animalsLoading } = useQuery<AnimalSummary[]>({
    queryKey: ['animals'],
    queryFn: getAnimals,
  });

  console.log(animals)
  return (
    <View activePanel={activePanel}>
      {/* 1) Панель СПИСКА */}
      <Panel id={DEFAULT_VIEW_PANELS.HOME}>
        {animalsLoading ? (
          <PanelSpinner />
        ) : (
          <AnimalList
            animals={animals}
            onItemClick={a => navigator.push(`/animals/${a}`)}
          />
        )}
      </Panel>

      {/* 2) Панель КАРТОЧКИ */}
      <Panel id={DEFAULT_VIEW_PANELS.ANIMAL}>
        {id ? (
          <AnimalCard
            id={DEFAULT_VIEW_PANELS.ANIMAL}
            petId={id}
            onBack={() => navigator.back()}
          />
        ) : (
          <Div style={{ padding: 16 }}>Животное не найдено</Div>
        )}
      </Panel>
    </View>
  );
};

export default App;
