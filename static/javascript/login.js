send = async () => {
  const cat = document.getElementById("cat").value;

  
  let response = await fetch('http://127.0.0.1:8000/data', {
      method: "POST",
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({"cat": cat}) // Отправляем email в формате JSON
  });

  try {
      const data = await response.json(); // Необходимо извлечь данные из ответа
      console.log(data);
  } catch (error) {
      console.error("Error parsing JSON:", error);
  }
};