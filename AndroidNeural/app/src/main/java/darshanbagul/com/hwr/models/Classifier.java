package darshanbagul.com.hwr.models;



public interface Classifier {
    String name();

    Classification recognize(final float[] pixels);
}