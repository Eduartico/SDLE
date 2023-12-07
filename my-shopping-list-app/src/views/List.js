import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ApiService from '../services/ApiService';
import BottomAppBar from '../components/BottomAppBar';

const List = () => {
  const { listId } = useParams();
  const [list, setList] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchList = async () => {
      try {
        const response = await ApiService.getListById(listId);
        setList(response.data.list);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching list:', error);
        setError('An error occurred while fetching the list.');
        setLoading(false);
      }
    };

    fetchList();
  }, [listId]);

  const handleQuantityChange = (itemId, newQuantity) => {
    setList((prevList) => {
      const updatedItems = prevList.items.map((item) => {
        if (item.id === itemId) {
          const boughtQuantity = Math.max(0, Math.min(newQuantity, item.quantity));
          return { ...item, boughtQuantity };
        }
        return item;
      });

      return { ...prevList, items: updatedItems };
    });
  };

  const handleToggleDone = (itemId) => {
    setList((prevList) => {
      const updatedItems = prevList.items.map((item) => {
        if (item.id === itemId) {
          const newBoughtQuantity = item.boughtQuantity === item.quantity ? 0 : item.quantity;
          return { ...item, boughtQuantity: newBoughtQuantity };
        }
        return item;
      });

      return { ...prevList, items: updatedItems };
    });
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  return (
    <div>
      <h2>List Name: {list.name}</h2>

      <h3>Done</h3>
      <ul>
        {list.items
          .filter((item) => item.boughtQuantity === item.quantity)
          .map((item) => (
            <li key={item.id}>
              <div style={{ display: 'flex', alignItems: 'inline' }}>
                <strong>{item.name}</strong>
                <div style={{ cursor: 'pointer', marginLeft: '5px' }} > Needed:  {item.quantity} </div>
                <label>
                  <input
                    type="checkbox"
                    checked={item.boughtQuantity === item.quantity}
                    onChange={() => handleToggleDone(item.id)}
                  />
                  Bought:
                </label>
                {item.quantity > 1 && (
                  <label>
                    <div>
                      <button
                        onClick={() => handleQuantityChange(item.id, Math.max(1, item.boughtQuantity - 1))}
                        style={{ cursor: 'pointer', marginLeft: '5px' }}
                      >
                        -
                      </button>
                      <input
                        type="number"
                        value={item.boughtQuantity}
                        onChange={(e) => handleQuantityChange(item.id, parseInt(e.target.value, 10))}
                        min="0"
                        max={item.quantity}
                        inputMode="numeric"
                        style={{ width: '50px', textAlign: 'center' }}
                      />
                      <button
                        onClick={() => handleQuantityChange(item.id, item.boughtQuantity + 1)}
                        style={{ cursor: 'pointer' }}
                      >
                        +
                      </button>
                    </div>
                  </label>
                )}
              </div>
            </li>
          ))}
      </ul>
      <h3>Needed</h3>
      <ul>
        {list.items
          .filter((item) => item.boughtQuantity < item.quantity)
          .map((item) => (
            <li key={item.id}>
              <div style={{ display: 'flex', alignItems: 'inline' }}>
                <strong>{item.name}</strong>
                <div style={{ cursor: 'pointer', marginLeft: '5px' }} > Needed:  {item.quantity} </div>
                <label>
                  <input
                    type="checkbox"
                    checked={item.boughtQuantity === item.quantity}
                    onChange={() => handleToggleDone(item.id)}
                  />
                  Bought:
                </label>
                {item.quantity > 1 && (
                  <label>
                    <div>
                      <button
                        onClick={() =>
                          handleQuantityChange(item.id, Math.max(1, item.boughtQuantity - 1))
                        }
                        style={{ cursor: 'pointer', marginLeft: '5px' }}
                      >
                        -
                      </button>
                      <input
                        type="number"
                        value={item.boughtQuantity}
                        onChange={(e) => handleQuantityChange(item.id, parseInt(e.target.value, 10))}
                        min="0"
                        max={item.quantity}
                        inputMode="numeric"
                        style={{ width: '50px', textAlign: 'center' }}
                      />
                      <button
                        onClick={() => handleQuantityChange(item.id, item.boughtQuantity + 1)}
                        style={{ cursor: 'pointer' }}
                      >
                        +
                      </button>
                    </div>
                  </label>
                )}
              </div>
            </li>
          ))}
      </ul>
      <div
        style={{
          position: 'fixed',
          bottom: 0,
          left: 0,
          width: '100%',
          background: '#f0f0f0',
          padding: '10px',
        }}
      >
        <BottomAppBar />
      </div>
    </div>
  );
};

export default List;
