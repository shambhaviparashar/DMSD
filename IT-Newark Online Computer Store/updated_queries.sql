CREATE DATABASE dmsd_final;

USE dmsd_final;

CREATE TABLE CUSTOMER (
	CID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Fname VARCHAR(25) NOT NULL,
    Lname VARCHAR(25) NOT NULL,
    Email VARCHAR(25) NOT NULL,
    Address VARCHAR(50) NOT NULL,
    Phone VARCHAR(10) NOT NULL,
    Status VARCHAR(10) DEFAULT 'Silver',
    Password varchar(255) NOT NULL
);

CREATE TABLE PRODUCT (
	ProductID INT NOT NULL PRIMARY KEY,
	Pname VARCHAR(50) NOT NULL,
    PPrice int,
    PType VARCHAR(25) NOT NULL,
    PQuantity INT NOT NULL,
    PDescription VARCHAR(200) NOT NULL
);

CREATE TABLE CREDIT_CARD (
	CardNumber VARCHAR(16) NOT NULL PRIMARY KEY,
    SecNumber  VARCHAR(3) NOT NULL,
    CardOwnerName VARCHAR(25) NOT NULL,
    CardType VARCHAR(10) NOT NULL,
    BillingAddress VARCHAR(50) NOT NULL,
    ExpDate Date NOT NULL,
    CID INT NOT NULL,
    FOREIGN KEY (CID) REFERENCES CUSTOMER (CID)
);

CREATE TABLE SHIP_ADDRESS (
	SAName VARCHAR(25) NOT NULL PRIMARY KEY,
    CID INT NOT NULL,
    RecipientName VARCHAR(25),
    SNumber VARCHAR(25),
    Street VARCHAR(25),
    Zip VARCHAR(10),
    City  VARCHAR(25),
    State VARCHAR(25),
    Country VARCHAR(25),
	FOREIGN KEY (CID) REFERENCES CUSTOMER (CID)
);

CREATE TABLE CART (
	CartID  INT NOT NULL PRIMARY KEY,
    TStatus VARCHAR(10) NOT NULL,
    TDate DATE,
    TotalAmount INT NOT NULL,
    CardNumber VARCHAR(12) NOT NULL,
    SAName VARCHAR(25) NOT NULL,
    CID INT NOT NULL,
    FOREIGN KEY (CID) REFERENCES CUSTOMER (CID),
    FOREIGN KEY (CardNumber) REFERENCES CREDIT_CARD (CardNumber),
    FOREIGN KEY (SAName) REFERENCES SHIP_ADDRESS (SAName)
);

CREATE TABLE STORED_CARD (
	CardNumber VARCHAR(12) NOT NULL PRIMARY KEY,
    StoredCardFlag VARCHAR(10),
	CID INT NOT NULL,
    FOREIGN KEY (CID) REFERENCES CUSTOMER (CID),
    FOREIGN KEY (CardNumber) REFERENCES CREDIT_CARD (CardNumber)
);

CREATE TABLE APPEARS_IN (
	CartID  INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    PriceSold INT NOT NULL,
    FOREIGN KEY (CartID) REFERENCES CART (CartID),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID)
);

CREATE TABLE OFFER_PRODUCT (
	ProductID INT NOT NULL PRIMARY KEY,
    OfferPrice INT NOT NULL,
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID)
);

CREATE TABLE DESKTOP (
	ProductID INT NOT NULL PRIMARY KEY,
    CPU VARCHAR(100),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID)
);

CREATE TABLE PRINTER (
	ProductID INT NOT NULL PRIMARY KEY,
    Resolution VARCHAR(50),
    PrinterType VARCHAR(150),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID)
);

CREATE TABLE LAPTOP (
	ProductID INT NOT NULL PRIMARY KEY,
    CPU VARCHAR(100),
    BatteryRunningTime VARCHAR(50),
    Weight VARCHAR(50),
    FOREIGN KEY (ProductID) REFERENCES PRODUCT (ProductID)
);

CREATE TABLE SILVER_AND_ABOVE (
	CartID  INT NOT NULL PRIMARY KEY,
    CreditLine VARCHAR(50),
    FOREIGN KEY (CartID) REFERENCES CART (CartID)
);



INSERT INTO
    PRODUCT (
        ProductID,
        Pname,
        PPrice,
        PType,
        PQuantity,
        PDescription
    )
VALUES (
        1,
        'Single-Pedestal Teacher Desk',
        '380',
        'Desk',
        1,
        'The Single-Pedestal Teacher Desk is a sleek, durable desk from Learniture. Attach the pedestal to the left or right side to customize your desk.'
    );

INSERT INTO `product` (`ProductID`, `PName`, `PType`, `Quantity`, `PPrice`, `PDescription`) VALUES
(1, 'Gaming Laptop XYZ', 'Laptop', 50, 1200.00, 'High-performance gaming laptop with dedicated GPU'),
(2, 'Office Laptop ABC', 'Laptop', 50, 1100.00, 'Business laptop with long battery life'),
(3, 'Inkjet Printer 123', 'Printer', 30, 150.00, 'Color inkjet printer for home use'),
(4, 'Laser Printer 456', 'Printer', 40, 200.00, 'Monochrome laser printer for office'),
(5, 'Desktop PC Core i7', 'Desktop', 20, 800.00, 'Powerful desktop computer for multitasking'),
(6, 'All-in-One Desktop XYZ', 'Desktop', 25, 1000.00, 'All-in-one desktop with touchscreen display'),
(7, 'Convertible Laptop ABC', 'Laptop', 45, 1300.00, 'Convertible laptop with touch display'),
(8, 'Wireless Printer XYZ', 'Printer', 35, 180.00, 'Wireless multifunction printer for home office'),
(9, 'Compact Desktop 123', 'Desktop', 30, 900.00, 'Compact desktop for small spaces'),
(10, 'High-End Gaming Laptop', 'Laptop', 55, 1400.00, 'High-end gaming laptop with RGB keyboard'),
(11, 'Photo Printer ABC', 'Printer', 25, 120.00, 'High-speed photo printer for photographers'),
(12, 'Business Desktop XYZ', 'Desktop', 28, 950.00, 'Business desktop with ample storage'),
(13, 'Ultra-thin Laptop ABC', 'Laptop', 60, 1500.00, 'Ultra-thin and portable laptop for professionals'),
(14, 'Compact Laser Printer XYZ', 'Printer', 22, 170.00, 'Compact laser printer for small offices'),
(15, 'Professional Desktop ABC', 'Desktop', 32, 1100.00, 'Performance desktop for professional tasks');

INSERT INTO `desktop` (`ProductID`, `CPU`) VALUES
(5, 'Intel Core i5'),
(6, 'AMD Ryzen 7'),
(9, 'Intel Core i7'),
(12, 'AMD Ryzen 5'),
(15, 'Intel Core i9');

INSERT INTO `laptop` (`ProductID`, `CPU`, `BatteryRunningTime`) VALUES
(1, 'Intel Core i5', '8 hours'),
(2, 'AMD Ryzen 7', '10 hours'),
(10, 'Intel Core i7', '12 hours'),
(13, 'AMD Ryzen 5', '9 hours');

INSERT INTO `printer` (`ProductID`, `Resolution`, `PrinterType`) VALUES
(3, '1200x1200 dpi', 'Inkjet'),
(4, '2400x600 dpi', 'Laser'),
(8, '4800x1200 dpi', 'Inkjet'),
(11, '600x600 dpi', 'Laser'),
(14, '300x300 dpi', 'Dot Matrix');

INSERT INTO `OFFER_PRODUCT` (`ProductID`, `OfferPrice`) VALUES
(1, 1100.00),
(4, 45.00),
(7, 22.50),
(9, 40.00),
(11, 30.00),
(13, 80.00);


-- Query 1: Compute the total amount charged per credit card. 
select c.CardNumber, sum(a.Quantity*a.PriceSold) as Amount_charged_per_card
from CART c
inner join APPEARS_IN a
on c.CartID = a.CartID
group by CardNumber


select CID, SUM(TotalAmount) from cart where TStatus = %s group by CID order by SUM(TotalAmount) DESC LIMIT 10;', ('Done')

SELECT ProductID, SUM(Quantity) FROM APPEARS_IN a, CART c WHERE a.CartID = c.CartID AND TStatus = % s AND TDate BETWEEN % s AND % s GROUP BY ProductID ORDER BY SUM(Quantity) DESC;',('Done', begindate, enddate)

select ProductID, COUNT(DISTINCT CID) from appears_in a, cart c where a.CartID = c.CartID and TStatus = %s and TDate BETWEEN %s and %s group by ProductID order by COUNT(DISTINCT CID) desc;',('Done', str(begindate), str(enddate))
        cursor.execute('select ProductID, COUNT(DISTINCT CID) from appears_in a, cart c where a.CartID = c.CartID and TStatus = %s and TDate BETWEEN %s and %s group by ProductID order by COUNT(DISTINCT CID) desc;',('Done', str(begindate), str(enddate)))


SELECT 
    c.CardNumber,
    MAX(c.TotalAmount) AS MaxBasketTotalAmount
FROM 
    CART c
WHERE 
    c.TDate BETWEEN %s AND %s
GROUP BY 
    c.CardNumber,(begindate, enddate)
    

'select PType, AVG(PPrice) from PRODUCT group by PType;'