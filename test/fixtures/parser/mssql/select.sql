SELECT
    [Name],
    [ProductNumber],
    ListPrice AS Price
  FROM [Production].[Product]
  WHERE [ProductLine] = 'R'
    AND DaysToManufacture < 4
  ORDER BY Name ASC