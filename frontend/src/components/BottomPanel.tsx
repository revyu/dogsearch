import { FC } from 'react';
import { Div, Button, FixedLayout } from '@vkontakte/vkui';
import { Icon28UserOutline, Icon28AddOutline } from '@vkontakte/icons';

export const BottomPanel: FC = () => {
  return (
    <FixedLayout vertical="bottom" filled>
      <Div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <Button before={<Icon28AddOutline />} mode="secondary" size="l">
          Добавить животное
        </Button>
        <Button before={<Icon28UserOutline />} mode="secondary" size="l">
          Профиль
        </Button>
      </Div>
    </FixedLayout>
  );
};