package uy.edu.um;

public class ProcesadorDeEnvio {
    public void enviarPedido(Pedido pedido) {
        System.out.println("Enviando pedido " + pedido.getId());
        try {
            Thread.sleep(100); // Simula el tiempo de envío
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
