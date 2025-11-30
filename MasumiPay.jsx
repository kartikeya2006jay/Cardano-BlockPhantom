// src/components/MasumiPay.jsx
import axios from 'axios';
import React, {useState} from 'react';

export default function MasumiPay({chain, address}) {
  const [loading, setLoading] = useState(false);
  const [payment, setPayment] = useState(null);

  const startPayment = async () => {
    if(!address) return alert("Enter address");
    setLoading(true);
    try {
      const res = await axios.post('/masumi/create-payment', {chain, address, currency: 'ADA', amount: 1000000});
      setPayment(res.data);
      // if Masumi returns a pay_url:
      if(res.data.pay_url) window.open(res.data.pay_url, '_blank');
    } catch(e) {
      alert("Payment init failed: "+e?.message);
    } finally { setLoading(false); }
  }

  async function check(paymentId) {
    const r = await axios.get(`/masumi/payment-status/${paymentId}`);
    return r.data;
  }

  const pollUntilPaid = async () => {
    if(!payment) return;
    let status = await check(payment.id);
    const start = Date.now();
    while(status?.status !== 'paid' && Date.now() - start < 2*60*1000) {
      await new Promise(r=>setTimeout(r,3000));
      status = await check(payment.id);
    }
    if(status?.status === 'paid') {
      alert('Payment confirmed — your PDF will be delivered.');
      // call backend endpoint to generate/download PDF (e.g., /report)
      window.open(`/report?chain=${encodeURIComponent(chain)}&address=${encodeURIComponent(address)}`, '_blank');
    } else {
      alert('Payment not confirmed in time.');
    }
  }

  return (
    <div>
      <button onClick={startPayment} disabled={loading}>Pay with Masumi</button>
      {payment && <button onClick={pollUntilPaid}>Check Payment & Download</button>}
    </div>
  );
}
