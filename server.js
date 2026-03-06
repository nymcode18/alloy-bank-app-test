const express = require('express');
const path = require('path');

const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

const ALLOY_TOKEN  = 'YOUR_TOKEN_HERE';
const ALLOY_SECRET = 'YOUR_SECRET_HERE';

const credentials = Buffer.from(`${ALLOY_TOKEN}:${ALLOY_SECRET}`).toString('base64');

app.post('/apply', async (req, res) => {
  const formData = req.body;
  try {
    const alloyResponse = await fetch('https://sandbox.alloy.co/v1/evaluations/', {
      method: 'POST',
      headers: {
        'Authorization': `Basic ${credentials}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name_first:           formData.name_first,
        name_last:            formData.name_last,
        email_address:        formData.email_address,
        birth_date:           formData.birth_date,
        document_ssn:         formData.document_ssn,
        address_line_1:       formData.address_line_1,
        address_line_2:       formData.address_line_2 || '',
        address_city:         formData.address_city,
        address_state:        formData.address_state,
        address_postal_code:  formData.address_postal_code,
        address_country_code: 'US'
      })
    });
    const result = await alloyResponse.json();
    const outcome = result?.summary?.outcome || 'Unknown';
    res.json({ outcome });
  } catch (error) {
    console.error('Error calling Alloy API:', error);
    res.status(500).json({ outcome: 'Error', message: 'Something went wrong.' });
  }
});

app.listen(PORT, () => {
  console.log(`✅ Server running at http://localhost:${PORT}`);
});