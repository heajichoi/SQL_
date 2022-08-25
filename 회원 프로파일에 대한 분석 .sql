USE PRACTICE;

# 회원수 추출 
/* 1. Customer 테이블의 가입연도별 및 지역별 회원수 */

  SELECT  YEAR(join_date) AS 연도
		  ,ADDR AS 지역
          ,COUNT(MEM_NO) AS 회원수
    FROM  CUSTOMER
   WHERE  GENDER='MAN'
   GROUP
      BY  year(join_date)
		  ,ADDR
  HAVING  COUNT(MEM_NO)>50
   ORDER
      BY  COUNT(MEM_NO) DESC;

/* 2. SELECT + JOIN */
   SELECT  B.BRAND
		   ,SUM(SALES_QTY) AS 판매
     FROM  SALES AS A
     LEFT
     JOIN  PRODUCT AS B
       ON  A.PRODUCT_CODE=B.PRODUCT_CODE
	GROUP
       BY  B.BRAND;
      
   SELECT  COUNT(A.MEM_NO)
     FROM  CUSTOMER AS A
     LEFT
     JOIN  SALES AS B
       ON  A.MEM_NO=B.MEM_NO
	WHERE  B.MEM_NO IS NULL;
    
/* 1. FROM절 서브쿼리를 활용하여, SALES 테이블의 PRODUCT_CODE별 판매수량 구하기
/* FROM절 서브쿼리 / SUM 함수 활용 */
   SELECT  BRAND
		   ,CATEGORY
           ,SUM(판매수량)AS 판매수량
     FROM  (
		   SELECT  PRODUCT_CODE
				   ,SUM(SALES_QTY) AS 판매수량
			 FROM  SALES
			GROUP
			   BY  PRODUCT_CODE
		    )AS A
	  LEFT
      JOIN  PRODUCT AS B
        ON  A.PRODUCT_CODE = B.PRODUCT_CODE
	 GROUP
        BY  BRAND
            ,CATEGORY;