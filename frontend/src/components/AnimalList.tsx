import { FC } from 'react';
import { Group, Cell, Avatar, Div, Link } from '@vkontakte/vkui';
import { Icon28ChevronRightOutline } from '@vkontakte/icons';

export interface AnimalSummary {
  pet_id: string;
  name: string;
  descriptions: string[];
  gender: string;
  images: string[];
  user_id: string;
}

interface AnimalListProps {
  animals: AnimalSummary[];
  onItemClick?: (petId: string) => void;
}

export const AnimalList: FC<AnimalListProps> = ({ animals, onItemClick }) => {
  return (
    <Group>
      {animals.length > 0 ? (
        animals.map((animal) => {
          // Собираем URL для удобства
          const petUrl = `https://petsi.app/ru/pet-details/${animal.pet_id}`;

          return (
            <Cell
              key={animal.pet_id}
              before={<Avatar size={48} src={animal.images[0]} />}
              after={<Icon28ChevronRightOutline />}
              onClick={() => onItemClick?.(animal.pet_id)}
              subtitle={
                <>
                  <div>Пол: {animal.gender}</div>
                  <div>Описание: {animal.descriptions.join(', ')}</div>
                  <div>
                    Ссылка:{' '}
                    {/* VKUI-компонент Link */}
                    <Link href={petUrl} target="_blank" rel="noopener noreferrer">
                      Перейти
                    </Link>
                  </div>
                </>
              }
            >
              {animal.name}
            </Cell>
          );
        })
      ) : (
        <Div>Животные не найдены</Div>
      )}
    </Group>
  );
};
