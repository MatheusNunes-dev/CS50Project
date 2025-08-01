fetch("/city_datas")
  .then(res => res.json())
  .then(({ values }) => {
    const data = {
      labels: ["City Tier 3", "City Tier 2", "City Tier 1"],
      datasets: [{
        label: 'Distribuição por Cidade',
        data: values,
        backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']
      }]
    };

    const config = {
      type: 'doughnut',
      data: data,
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top'
          },
          title: {
            display: true,
            text: 'Predicts Chunrs by City Tier'
          }
        }
      }
    };

    new Chart(document.getElementById("myChart"), config);
  });

