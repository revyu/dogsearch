import { useState, useEffect } from 'react';
import { View, Panel, PanelHeader, Tabs, TabsItem, Search } from '@vkontakte/vkui';
import { AnimalList } from './components/AnimalList';
import { BottomPanel } from './components/BottomPanel';

export const App = () => {
  const [activeTab, setActiveTab] = useState<'list' | 'map'>('list');
  const [search, setSearch] = useState('');
  const [animalsData, setAnimalsData] = useState([]);

  // Функция для загрузки данных с бэкенда
  useEffect(() => {
    const fetchAnimals = async () => {
      try {
        const response = await fetch('http://localhost:8000/animals'); // Замените на ваш URL
        if (!response.ok) {
          throw new Error('Ошибка при загрузке данных');
        }
        const data = await response.json();
        setAnimalsData(data);
      } catch (error) {
        console.error('Ошибка:', error);
      }
    };

    fetchAnimals();
  }, []);

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