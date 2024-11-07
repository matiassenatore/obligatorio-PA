package uy.edu.um;

public class ProcesadorDePago {
    public void procesarPago(Pedido pedido) {
        System.out.println("Procesando pago para el pedido " + pedido.getId());
        try {
            Thread.sleep(100); // Simula el tiempo de procesamiento
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
