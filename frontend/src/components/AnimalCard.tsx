import { FC, useEffect, useState } from 'react';
import {
  Panel,
  PanelHeader,
  Group,
  Title,
  Div,
  Avatar,
  FixedLayout,
  Button,
  Spinner,
} from '@vkontakte/vkui';

export interface AnimalDetails {
  petId: number;
  name: string;
  gender: string;
  descriptions: string;
  images: string;
  address: string;
  user_id: string;
}

interface Props {
  id: string;
  petId: string; // Используем petId для запроса данных
  onBack: () => void;
}

export const AnimalCard: FC<Props> = ({ id, petId, onBack }) => {
  const [animal, setAnimal] = useState<AnimalDetails | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnimal = async () => {
      try {
        const response = await fetch(`http://localhost:5173/animals/${petId}`); // Получаем животное по ID
        const data = await response.json();
        setAnimal(data);
      } catch (error) {
        console.error('Ошибка при загрузке животного:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchAnimal();
  }, [petId]);

  if (loading) {
    return <Spinner />;
  }

  if (!animal) {
    return <Div>Животное не найдено</Div>;
  }

  // Генерация ссылки в нужном формате
  const petUrl = 'https://petsi.app/ru/pet-details/${animal.pet_id}';

  console.log(petId);
  console.log('AnimalCard mounted, petId =', petId);
  return (
    <Panel id={id}>
      <PanelHeader before={<span onClick={onBack}>Назад</span>}>Потерялся</PanelHeader>
      <Group>
        <Div style={{ display: 'flex', justifyContent: 'center' }}>
          <Avatar size={120} src={animal.images} />
        </Div>
        <Div>
          <Title level="3" weight="2">Кличка: {animal.name}</Title>
          <div>Описание: {animal.descriptions || 'отсутствует'}</div>
          <div>Адрес: {animal.address}</div>
          <div>Ссылка на животного: <a href={petUrl} target="_blank" rel="noopener noreferrer">{petUrl}</a></div>
        </Div>
      </Group>

      <FixedLayout vertical="bottom" filled>
        <Div style={{ display: 'flex', gap: 8 }}>
          <Button size="l" stretched mode="secondary">Я видел!</Button>
          <Button size="l" stretched mode="primary">Я нашел!</Button>
        </Div>
      </FixedLayout>
    </Panel>
  );
};