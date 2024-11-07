package uy.edu.um;

public class ProcesadorDeEmpaquetado {
    public void empacarPedido(Pedido pedido) {
        System.out.println("Empacando pedido " + pedido.getId());
        try {
            Thread.sleep(100); // Simula el tiempo de empaquetado
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
