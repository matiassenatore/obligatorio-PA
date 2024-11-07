package uy.edu.um;

public class Pedido implements Comparable<Pedido> {
    private final int id;
    private final int prioridad;  // 1 = urgente, 2 = normal

    public Pedido(int id, int prioridad) {
        this.id = id;
        this.prioridad = prioridad;
    }

    public int getId() {
        return id;
    }

    public int getPrioridad() {
        return prioridad;
    }

    @Override
    public String toString() {
        return "Pedido ID: " + id + " - Prioridad: " + (prioridad == 1 ? "Urgente" : "Normal");
    }

    @Override
    public int compareTo(Pedido o) {
        return Integer.compare(this.prioridad, o.prioridad); // Urgentes (1) se procesan antes que Normales (2)
    }
}
