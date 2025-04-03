import { FC } from 'react';
import { Group, Cell, Avatar, Div } from '@vkontakte/vkui';
import { Icon28ChevronRightOutline } from '@vkontakte/icons';

interface Animal {
  id: number;
  name: string;
  type: string;
  breed?: string;
  status: string;
  reward?: number;
  photo: string;
}

interface AnimalListProps {
  animals: Animal[];
}

export const AnimalList: FC<AnimalListProps> = ({ animals }) => {
  return (
    <Group>
      {animals.length > 0 ? (
        animals.map((animal) => (
            <Cell
            key={animal.id}
            before={<Avatar size={48} src={animal.photo} />}
            after={<Icon28ChevronRightOutline />}
            subtitle={
              <>
                <div>Животное: {animal.type}</div>
                <div>Порода: {animal.breed || 'отсутствует'}</div>
                <div>{animal.status}</div>
                <div>Награда: {animal.reward ? '400₽' : 'нет'}</div>
              </>
            }
          >
            {animal.name}
          </Cell>
        ))
      ) : (
        <Div>Животные не найдены</Div>
      )}
    </Group>
  );
};