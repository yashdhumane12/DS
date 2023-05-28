import java.rmi.Remote;
import java.rmi.RemoteException;
public interface Hello extends Remote{
	default void message() throws RemoteException{}
}