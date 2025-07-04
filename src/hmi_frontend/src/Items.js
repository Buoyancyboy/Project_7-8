import React, { useState } from 'react';
import SearchByTimestamp from './SearchByTimestamp';

export default function Items() {
  const [items, setItems] = useState([]);

  return (
    <div>
      <SearchByTimestamp onResults={setItems} />
      <ul>
        {items.map(item => (
          <li key={item.id}>
            {item.name}: {item.timestamp}
          </li>
        ))}
      </ul>
    </div>
  );
}
