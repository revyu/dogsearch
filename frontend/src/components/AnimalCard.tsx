import { FC } from 'react';
import {
  Panel,
  PanelHeader,
  Group,
  Title,
  Div,
  Avatar,
  FixedLayout,
  Button,
} from '@vkontakte/vkui';

interface Animal {
  id: number;
  name: string;
  type: string;
  breed?: string;
  status: string;
  reward?: number;
  photo: string;
  location: string;
  owner: string;
  postLink: string;
  description: string;
}

interface Props {
  id: string;
  animal: Animal;
  onBack: () => void;
}

export const AnimalCard: FC<Props> = ({ id, animal, onBack }) => {
  return (
    <Panel id={id}>
      <PanelHeader before={<span onClick={onBack}>Назад</span>}>Потерялся</PanelHeader>
      <Group>
        <Div style={{ display: 'flex', justifyContent: 'center' }}>
          <Avatar size={120} src={animal.photo} />
        </Div>
        <Div>
          <Title level="3" weight="2">Кличка: {animal.name}</Title>
          <div>Животное: {animal.type}</div>
          <div>Порода: {animal.breed || 'отсутствует'}</div>
          <div>Местоположение: {animal.location}</div>
          <div>Награда: {animal.reward ? '${animal.reward}₽' : 'нет'}</div>
          <div>Данные о хозяине: {animal.owner}</div>
          <div>Ссылка на пост: <a href={animal.postLink} target="_blank">{animal.postLink}</a></div>
          <div>Описание: {animal.description}</div>
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