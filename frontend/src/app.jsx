import { useState } from "react";
import OrdersUploader from "./components/OrdersUploader";
import OptimizeForm from "./components/OptimizeForm";
import RoutesView from "./components/RoutesView";

export default function App() {
  const [result, setResult] = useState(null);

  return (
    <div style={{maxWidth:900, margin:"0 auto", padding:24}}>
      <h1>PackRoute</h1>
      <OrdersUploader onUploaded={()=>{}} />
      <hr/>
      <OptimizeForm onResult={setResult} />
      <RoutesView data={result} />
    </div>
  );
}
