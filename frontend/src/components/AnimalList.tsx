import { FC } from 'react';
import { Group, Cell, Avatar, Div } from '@vkontakte/vkui';
import { Icon28ChevronRightOutline } from '@vkontakte/icons';

import type { AnimalSummary } from './Animal';

interface AnimalListProps {
  animals: AnimalSummary[];
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