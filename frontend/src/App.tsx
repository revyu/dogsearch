import { useState } from 'react';
import { View, Panel, PanelHeader, Tabs, TabsItem, Search } from '@vkontakte/vkui';
import { AnimalList } from './components/AnimalList';
import { BottomPanel } from './components/BottomPanel';

const animalsData = [
  {
    id: 1,
    name: 'Жорик',
    type: 'кот',
    breed: 'отсутствует',
    status: 'Потерян',
    reward: 400,
    photo: ' ',
  },
];

export const App = () => {
  const [activeTab, setActiveTab] = useState<'list' | 'map'>('list');
  const [search, setSearch] = useState('');
  const filteredAnimals = animalsData.filter((animal) =>
    animal.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <View activePanel="main">
      <Panel id="main">
        <PanelHeader>Поиск животных</PanelHeader>

        <Tabs>
          <TabsItem selected={activeTab === 'map'} onClick={() => setActiveTab('map')}>
            Карта
          </TabsItem>
          <TabsItem selected={activeTab === 'list'} onClick={() => setActiveTab('list')}>
            Список
          </TabsItem>
        </Tabs>

        <Search value={search} onChange={(e) => setSearch(e.target.value)} />

        {activeTab === 'list' && <AnimalList animals={filteredAnimals} />}

        <BottomPanel />
      </Panel>
    </View>
  );
};